#!/usr/bin/env python3
"""Run crypto OpenCLI source health checks and emit diagnostic events."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class SourceSpec:
    source_name: str
    source_category: str
    command: list[str]
    entity: str
    requested_fields: list[str]
    failure_repairs: dict[str, list[str]]
    fallback: "SourceSpec | None" = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_json(output: str) -> Any | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(output):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(output[index:])
            return value
        except json.JSONDecodeError:
            continue
    return None


def run_command(command: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return completed.returncode, completed.stdout or "", completed.stderr or ""
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return 124, stdout, stderr or f"Command timed out after {timeout}s"
    except FileNotFoundError as exc:
        return 127, "", str(exc)


def resolve_opencli() -> list[str] | None:
    for candidate in ("opencli", "opencli.cmd", "opencli.exe", "opencli.ps1"):
        path = shutil.which(candidate)
        if not path:
            continue
        if path.lower().endswith(".ps1"):
            powershell = shutil.which("powershell") or shutil.which("pwsh")
            if powershell:
                return [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path]
            return None
        return [path]
    return None


def detect_failure_reason(returncode: int, stdout: str, stderr: str, data: Any | None) -> str:
    combined = f"{stdout}\n{stderr}".lower()
    if returncode == 124:
        return "timeout"
    if "browser profile" in combined or "browser bridge" in combined or "profile" in combined and "not connected" in combined:
        return "browser_profile_disconnected"
    if "api_key" in combined or "token" in combined or "credential" in combined:
        return "missing_credentials"
    if "rate" in combined and "limit" in combined:
        return "rate_limit"
    if "schema" in combined or "missing expected" in combined:
        return "schema_drift"
    if "no data" in combined or data == [] or data is None:
        return "no_data"
    if returncode != 0:
        return "adapter_error"
    return "none"


def validate_rows(data: Any, expected_fields: list[str]) -> tuple[str, str]:
    if not isinstance(data, list) or not data:
        return "fail", "no rows"
    first = data[0]
    if not isinstance(first, dict):
        return "suspicious", "first row is not an object"
    missing = [field for field in expected_fields if field not in first]
    if missing:
        return "suspicious", f"missing expected fields: {', '.join(missing)}"
    non_null = [field for field in expected_fields if first.get(field) not in (None, "", [])]
    if not non_null:
        return "partial", "expected fields are present but empty"
    return "pass", "ok"


def infer_timestamp(data: Any) -> str | None:
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return None
    row = data[0]
    for field in ("timestamp", "tvlAt", "updatedAt", "time", "date"):
        if row.get(field):
            return str(row[field])
    return None


def repairs_for(spec: SourceSpec, reason: str) -> list[str]:
    return spec.failure_repairs.get(reason) or spec.failure_repairs.get("default", [])


def check_source(spec: SourceSpec, timeout: int) -> tuple[dict[str, Any], Any | None]:
    returncode, stdout, stderr = run_command(spec.command, timeout)
    data = extract_json(stdout)
    status, validation_note = validate_rows(data, spec.requested_fields)
    reason = detect_failure_reason(returncode, stdout, stderr, data)

    if returncode != 0:
        status = "fail"
    elif status != "pass" and reason == "none":
        reason = "schema_drift" if "missing expected" in validation_note else "no_data"

    event = {
        "source_name": spec.source_name,
        "source_category": spec.source_category,
        "command_or_access_path": " ".join(spec.command),
        "entity": spec.entity,
        "requested_fields": spec.requested_fields,
        "status": status,
        "observed_at": utc_now(),
        "data_timestamp": infer_timestamp(data),
        "failure_reason": reason if status != "pass" else "none",
        "fallback_used": "none",
        "user_message": "",
        "repair_candidates": [] if status == "pass" else repairs_for(spec, reason),
        "validation_note": validation_note,
    }

    if status == "pass":
        event["user_message"] = f"{spec.source_name} returned usable data for {spec.entity}."
    else:
        event["user_message"] = (
            f"{spec.source_name} returned {status} for {spec.entity}: "
            f"{event['failure_reason']}. Treat related conclusions as incomplete unless fallback data is used."
        )
    return event, data


def summarize(events: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [event["source_name"] for event in events if event["status"] != "pass"]
    fallbacks = [event["fallback_used"] for event in events if event.get("fallback_used") not in (None, "none")]
    status = "pass" if not failed else "partial"
    return {
        "status": status,
        "failed_sources": failed,
        "fallback_sources": fallbacks,
        "user_warning": (
            "All checked crypto sources returned usable data."
            if status == "pass"
            else "Some crypto sources failed or returned incomplete data; inspect diagnostic_events before relying on conclusions."
        ),
        "repair_candidates": sorted(
            {
                repair
                for event in events
                for repair in event.get("repair_candidates", [])
            }
        ),
    }


def build_specs(opencli_cmd: list[str], symbol: str, derivative_symbol: str, protocol: str, limit: int) -> list[SourceSpec]:
    common_repairs = {
        "adapter_error": ["run the same command with --trace retain-on-failure", "inspect opencli adapter help"],
        "timeout": ["retry once", "reduce result limit", "try fallback source"],
        "schema_drift": ["inspect returned fields", "update adapter field mapping", "try alternative command"],
        "no_data": ["normalize symbol", "try another venue", "try fallback source"],
        "browser_profile_disconnected": ["run opencli doctor", "connect Browser Bridge profile", "fall back to non-browser sources"],
        "default": ["try fallback source", "surface source limitation to user"],
    }
    derivatives_fallback = SourceSpec(
        source_name="CoinGecko derivatives",
        source_category="derivatives_aggregator",
        command=[*opencli_cmd, "coingecko", "derivatives", "--symbol", derivative_symbol, "--limit", str(limit), "-f", "json"],
        entity=derivative_symbol,
        requested_fields=["market", "symbol", "fundingRate", "openInterestUsd", "volume24hUsd"],
        failure_repairs=common_repairs,
    )
    return [
        SourceSpec(
            source_name="Binance price",
            source_category="exchange_direct",
            command=[*opencli_cmd, "binance", "price", symbol, "-f", "json"],
            entity=symbol,
            requested_fields=["symbol", "price", "change_pct", "volume", "quote_volume"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="Binance klines",
            source_category="exchange_direct",
            command=[*opencli_cmd, "binance", "klines", symbol, "--interval", "4h", "--limit", str(limit), "-f", "json"],
            entity=symbol,
            requested_fields=["open", "high", "low", "close", "volume"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="Binance depth",
            source_category="exchange_direct",
            command=[*opencli_cmd, "binance", "depth", symbol, "--limit", "5", "-f", "json"],
            entity=symbol,
            requested_fields=["bid_price", "bid_qty", "ask_price", "ask_qty"],
            failure_repairs=common_repairs,
        ),
        derivatives_fallback,
        SourceSpec(
            source_name="DefiLlama protocol",
            source_category="onchain_protocol",
            command=[*opencli_cmd, "defillama", "protocol", protocol, "-f", "json"],
            entity=protocol,
            requested_fields=["slug", "name", "category", "tvl", "chains"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="CoinGlass open interest",
            source_category="browser_source",
            command=[*opencli_cmd, "coinglass", "open-interest", "-f", "json"],
            entity=derivative_symbol,
            requested_fields=["symbol", "value", "source"],
            failure_repairs=common_repairs,
            fallback=derivatives_fallback,
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run crypto source health checks.")
    parser.add_argument("--symbol", default="ETHUSDT", help="Exchange pair, e.g. ETHUSDT")
    parser.add_argument("--derivative-symbol", default="ETH", help="Derivative filter symbol, e.g. ETH")
    parser.add_argument("--protocol", default="lido", help="DefiLlama protocol slug")
    parser.add_argument("--limit", type=int, default=5, help="Rows to request for list-like sources")
    parser.add_argument("--timeout", type=int, default=30, help="Command timeout in seconds")
    args = parser.parse_args()

    opencli_cmd = resolve_opencli()
    if opencli_cmd is None:
        result = {
            "source_health": {
                "status": "fail",
                "failed_sources": ["opencli"],
                "fallback_sources": [],
                "user_warning": "opencli is not available on PATH.",
                "repair_candidates": ["install opencli", "add opencli to PATH"],
            },
            "diagnostic_events": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    events: list[dict[str, Any]] = []
    for spec in build_specs(opencli_cmd, args.symbol, args.derivative_symbol, args.protocol, args.limit):
        event, _ = check_source(spec, args.timeout)
        if event["status"] != "pass" and spec.fallback is not None:
            fallback_event, _ = check_source(spec.fallback, args.timeout)
            events.append(fallback_event)
            if fallback_event["status"] == "pass":
                event["fallback_used"] = spec.fallback.source_name
                event["user_message"] += f" Fallback succeeded: {spec.fallback.source_name}."
        events.append(event)

    result = {
        "source_health": summarize(events),
        "diagnostic_events": events,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["source_health"]["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
