#!/usr/bin/env python3
"""
Calculate Month-To-Date (MTD) or period-over-period performance for an IOL portfolio.
Includes input validation and security hardening against malformed data.
"""

import argparse
import json
import math
import os
import sys

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit to prevent memory exhaustion

def parse_number(val, field_name, asset_name, default=0.0):
    """Safely parse and validate a finite numeric value."""
    if val is None:
        return default
    try:
        num = float(val)
        if not math.isfinite(num):
            raise ValueError("Value must be a finite number")
        return num
    except (TypeError, ValueError) as err:
        sys.stderr.write(f"Validation error for asset '{asset_name}' field '{field_name}': {err}\n")
        sys.exit(1)

def parse_currency(currency_val, asset_name):
    """Safely validate currency code."""
    if not isinstance(currency_val, str):
        return "ARS"
    sanitized = currency_val.strip().upper()
    if not sanitized.isalpha() or len(sanitized) > 5:
        sys.stderr.write(f"Invalid currency '{currency_val}' for asset '{asset_name}'. Defaulting to ARS.\n")
        return "ARS"
    return sanitized

def calculate_performance(start_data, end_data, external_inflows):
    """Calculates MTD earnings for ARS and USD assets."""
    total_start_ars = 0.0
    total_end_ars = 0.0
    total_start_usd = 0.0
    total_end_usd = 0.0

    print(f"{'Asset':<10} | {'Start Qty':<12} | {'Start Val':<12} | {'End Qty':<12} | {'End Val':<12} | {'Net Earnings':<12} | {'Currency':<4}")
    print("-" * 90)

    # Consider all unique assets present in start, end, or both
    all_assets = sorted(set(start_data.keys()).union(set(end_data.keys())))

    for asset in all_assets:
        raw_start = start_data.get(asset, {})
        raw_end = end_data.get(asset, {})

        if not isinstance(raw_start, dict):
            raw_start = {}
        if not isinstance(raw_end, dict):
            raw_end = {}

        currency = parse_currency(raw_start.get("currency") or raw_end.get("currency", "ARS"), asset)

        start_qty = parse_number(raw_start.get("qty", 0.0), "qty", asset)
        start_price = parse_number(raw_start.get("price", 0.0), "price", asset)
        end_qty = parse_number(raw_end.get("qty", 0.0), "qty", asset)
        end_price = parse_number(raw_end.get("price", 0.0), "price", asset)

        val_start = start_qty * start_price
        val_end = end_qty * end_price

        if currency == "ARS":
            total_start_ars += val_start
            total_end_ars += val_end
            earnings = val_end - val_start
        else:
            total_start_usd += val_start
            total_end_usd += val_end
            subs = parse_number(raw_start.get("net_purchases", 0.0), "net_purchases", asset)
            earnings = val_end - val_start - subs

        print(f"{asset:<10} | {start_qty:<12.4f} | {val_start:<12.2f} | {end_qty:<12.4f} | {val_end:<12.2f} | {earnings:<12.2f} | {currency:<4}")

    print("\n--- Portfolio Summary ---")
    print(f"Initial Valuation: {total_start_ars:,.2f} ARS  |  {total_start_usd:,.2f} USD")
    print(f"Ending Valuation:  {total_end_ars:,.2f} ARS  |  {total_end_usd:,.2f} USD")

    inflows_ars = parse_number(external_inflows.get("ARS", 0.0), "inflows.ARS", "EXTERNAL")
    inflows_usd = parse_number(external_inflows.get("USD", 0.0), "inflows.USD", "EXTERNAL")
    print(f"External Inflows:  {inflows_ars:,.2f} ARS  |  {inflows_usd:,.2f} USD")

    mtd_earnings_ars = (total_end_ars - total_start_ars) - inflows_ars
    mtd_earnings_usd = (total_end_usd - total_start_usd) - inflows_usd

    print(f"MTD Net Earnings:  {mtd_earnings_ars:,.2f} ARS  |  {mtd_earnings_usd:,.2f} USD")

def main():
    parser = argparse.ArgumentParser(description="Calculate portfolio MTD earnings with hardened input validation.")
    parser.add_argument("--portfolio", type=str, required=True, help="Path to portfolio JSON file containing start, end, and inflows data.")
    args = parser.parse_args()

    portfolio_path = os.path.abspath(args.portfolio)

    if not os.path.exists(portfolio_path):
        sys.stderr.write(f"Error: File does not exist: {portfolio_path}\n")
        sys.exit(1)

    if not os.path.isfile(portfolio_path):
        sys.stderr.write(f"Error: Path is not a regular file: {portfolio_path}\n")
        sys.exit(1)

    try:
        file_size = os.path.getsize(portfolio_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            sys.stderr.write(f"Error: File size ({file_size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE_BYTES} bytes)\n")
            sys.exit(1)

        with open(portfolio_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Invalid JSON format: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error reading portfolio file: {e}\n")
        sys.exit(1)

    if not isinstance(data, dict):
        sys.stderr.write("Error: Root JSON content must be an object/dict.\n")
        sys.exit(1)

    start_data = data.get("start") or {}
    end_data = data.get("end") or {}
    inflows = data.get("external_inflows") or {"ARS": 0.0, "USD": 0.0}

    if not isinstance(start_data, dict) or not isinstance(end_data, dict) or not isinstance(inflows, dict):
        sys.stderr.write("Error: 'start', 'end', and 'external_inflows' must be JSON objects.\n")
        sys.exit(1)

    calculate_performance(start_data, end_data, inflows)

if __name__ == "__main__":
    main()
