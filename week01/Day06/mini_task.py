"""
Week 1 Mini-Task: Stock Analyser (no Pandas)
Stock: RELIANCE.NS  |  Period: Jan–Feb 2025
Author: [Your Name]  |  Date: 2025-01-xx
"""

import csv
import os

# ── Config ────────────────────────────────────────────────────────────────────
CSV_FILE = os.path.join(os.path.dirname(__file__), "RELIANCE.csv")
CLOSE_COL = "Close"
DATE_COL  = "Date"


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_csv(filepath: str) -> list[dict]:
    """Read CSV into a list of row-dicts (all values are strings)."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def to_float(value: str) -> float:
    return float(value.strip())


# ── Analysis functions ────────────────────────────────────────────────────────
def total_trading_days(rows: list[dict]) -> int:
    return len(rows)


def average_close(rows: list[dict]) -> float:
    prices = [to_float(r[CLOSE_COL]) for r in rows]
    return sum(prices) / len(prices)


def highest_close(rows: list[dict]) -> tuple[float, str]:
    best = max(rows, key=lambda r: to_float(r[CLOSE_COL]))
    return to_float(best[CLOSE_COL]), best[DATE_COL]


def lowest_close(rows: list[dict]) -> tuple[float, str]:
    worst = min(rows, key=lambda r: to_float(r[CLOSE_COL]))
    return to_float(worst[CLOSE_COL]), worst[DATE_COL]


def total_return_pct(rows: list[dict]) -> float:
    first_close = to_float(rows[0][CLOSE_COL])
    last_close  = to_float(rows[-1][CLOSE_COL])
    return ((last_close - first_close) / first_close) * 100


# ── Display ───────────────────────────────────────────────────────────────────
DIVIDER   = "─" * 52
BOLD_DIV  = "═" * 52

def print_report(rows: list[dict]) -> None:
    days            = total_trading_days(rows)
    avg             = average_close(rows)
    high, high_date = highest_close(rows)
    low,  low_date  = lowest_close(rows)
    ret_pct         = total_return_pct(rows)

    first_close = to_float(rows[0][CLOSE_COL])
    last_close  = to_float(rows[-1][CLOSE_COL])
    period      = f"{rows[0][DATE_COL]}  →  {rows[-1][DATE_COL]}"

    print()
    print(BOLD_DIV)
    print("  📈  RELIANCE INDUSTRIES — STOCK ANALYSIS")
    print(BOLD_DIV)
    print(f"  Period  : {period}")
    print(DIVIDER)

    # (a) Total trading days
    print(f"  (a) Total Trading Days     :  {days}")

    # (b) Average closing price
    print(f"  (b) Average Closing Price  :  ₹{avg:>10.2f}")

    # (c) Highest / Lowest
    print(f"  (c) Highest Closing Price  :  ₹{high:>10.2f}  [{high_date}]")
    print(f"      Lowest  Closing Price  :  ₹{low:>10.2f}  [{low_date}]")
    print(f"      Price Range            :  ₹{high - low:>10.2f}")

    # (d) Total return
    arrow = "▲" if ret_pct >= 0 else "▼"
    print(f"  (d) Total Return           :  {arrow} {abs(ret_pct):>7.2f}%")
    print(f"      Entry Price            :  ₹{first_close:>10.2f}  [{rows[0][DATE_COL]}]")
    print(f"      Exit  Price            :  ₹{last_close:>10.2f}  [{rows[-1][DATE_COL]}]")
    print(f"      Absolute Gain          :  ₹{last_close - first_close:>10.2f}")

    print(BOLD_DIV)
    print()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rows = load_csv(CSV_FILE)

    if not rows:
        print("ERROR: CSV file is empty or could not be loaded.")
        raise SystemExit(1)

    print_report(rows)
