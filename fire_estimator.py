#!/usr/bin/env python3
"""
FIRE (Financial Independence, Retire Early) Estimator

FIRE is achieved when 4% of your investment portfolio (COI) covers annual expenses.
Simulation runs month by month. Set AROI in the definition area; MROI is derived automatically.

Usage:
  python fire_estimator.py                          # fn1 (default)
  python fire_estimator.py --fn1                    # estimate months/years to FIRE
  python fire_estimator.py --fn2 "3 5000 0" "7 0 10000"  # re-estimate with UE/UI events (month-based)
  python fire_estimator.py --fn3                          # generate 4 plots (AROI / expenditure / salary / risk tolerance)
"""

import argparse
import os

import matplotlib.pyplot as plt

# ===========================================================================
# DEFINITION AREA — modify your variables here
# ===========================================================================

OUTPUT_DIR       = "outputs"   # Directory for all log files and plots

CURRENCY         = "CNY"       # Currency type (e.g. "USD", "AUD", "CNY")

INITIAL_CASH     = 30_000      # Initial cash amount at the starting moment
INITIAL_COI      = 14_100      # COI (investment portfolio) at the starting moment
MONTHLY_SALARY   = 32_111      # Monthly salary after tax
AROI             = 0.10        # Annual Return of Investment (e.g. 0.10 = 10%)
MROI             = (1 + AROI) ** (1 / 12) - 1  # Derived from AROI — do not edit
RISK_TOLERANCE   = 0.50        # Fraction of salary to invest (e.g. 0.50 = 50%)

RENT_COSTS       = 7_309.07    # Monthly rent
UTILITIES        = 505         # Monthly utilities
INTERNET_COSTS   = 383         # Monthly internet
FOOD_COSTS       = 4_334       # Monthly food
TRANSPORTATION   = 1_060       # Monthly transportation
MOBILE_PLAN      = 160         # Monthly mobile phone plan

# ===========================================================================


# ---------------------------------------------------------------------------
# Core formulas
# ---------------------------------------------------------------------------

MONTHLY_EXPENDITURE = RENT_COSTS + UTILITIES + INTERNET_COSTS + FOOD_COSTS + TRANSPORTATION + MOBILE_PLAN

os.makedirs(OUTPUT_DIR, exist_ok=True)

def _compute_month(coi, remaining_cash, salary=None, ue=0, ui=0):
    """
    Simulate one month and return (new_coi, new_cash, total_assets).

    Cash Earned This Month  = Monthly Salary × (1 - Risk Tolerance Rate)
    COI Appended This Month = Monthly Salary × Risk Tolerance Rate
    Total Cash              = Remaining Cash + Cash Earned + UI - UE
    COI (updated)           = (Current COI + COI Appended) × (1 + MROI)
    Remaining Cash          = Total Cash - Monthly Expenditure
    Total Assets            = COI + Remaining Cash
    """
    if salary is None:
        salary = MONTHLY_SALARY
    cash_earned  = salary * (1 - RISK_TOLERANCE)
    coi_appended = salary * RISK_TOLERANCE

    total_cash = remaining_cash + cash_earned + ui - ue
    new_coi    = coi * (1 + MROI) + coi_appended
    new_cash   = total_cash - MONTHLY_EXPENDITURE

    return new_coi, new_cash, new_coi + new_cash


def _fire_achieved(coi):
    """4% annual withdrawal from COI must cover annual expenditure."""
    return 0.04 * coi >= 12 * MONTHLY_EXPENDITURE


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def _fmt(amount):
    return f"{CURRENCY} {amount:>14,.2f}"


def _yr_mo(month):
    """Format month number as 'Yr X, Mo Y'."""
    return f"Yr {(month - 1) // 12 + 1:>3}, Mo {(month - 1) % 12 + 1:>2}"


def _fire_duration(month):
    yrs, mos = divmod(month, 12)
    return f"{yrs} year(s) and {mos} month(s)"


def _log_month(month, prev_coi, prev_cash, salary, log_file, ue=0, ui=0):
    """Write step-by-step calculation log for one simulated month to log_file."""
    cash_earned  = salary * (1 - RISK_TOLERANCE)
    coi_appended = salary * RISK_TOLERANCE
    total_cash   = prev_cash + cash_earned + ui - ue
    new_coi      = prev_coi * (1 + MROI) + coi_appended
    new_cash     = total_cash - MONTHLY_EXPENDITURE
    passive_mo   = 0.04 * new_coi / 12
    progress_pct = min(passive_mo / MONTHLY_EXPENDITURE * 100, 100)

    p = lambda s: print(s, file=log_file)
    p(f"\n  [{_yr_mo(month)}]" + (f"  ** UE: {_fmt(ue)}  UI: {_fmt(ui)} **" if ue or ui else ""))
    p(f"    Cash Earned      = {_fmt(salary)} × {1 - RISK_TOLERANCE:.0%}  →  {_fmt(cash_earned)}")
    p(f"    COI Appended     = {_fmt(salary)} × {RISK_TOLERANCE:.0%}  →  {_fmt(coi_appended)}")
    if ue or ui:
        p(f"    Total Cash       = {_fmt(prev_cash)} + {_fmt(cash_earned)}"
          f" + UI {_fmt(ui)} - UE {_fmt(ue)}  →  {_fmt(total_cash)}")
    else:
        p(f"    Total Cash       = {_fmt(prev_cash)} + {_fmt(cash_earned)}  →  {_fmt(total_cash)}")
    p(f"    COI (updated)    = {_fmt(prev_coi)} × {1 + MROI:.5f} + {_fmt(coi_appended)}  →  {_fmt(new_coi)}")
    p(f"    Remaining Cash   = {_fmt(total_cash)} - {_fmt(MONTHLY_EXPENDITURE)}  →  {_fmt(new_cash)}")
    p(f"    Total Assets     = {_fmt(new_coi)} + {_fmt(new_cash)}  →  {_fmt(new_coi + new_cash)}")
    p(f"    Passive income   = {_fmt(passive_mo)} / mo"
      f"   (need {_fmt(MONTHLY_EXPENDITURE)})   [{progress_pct:.1f}% to FIRE]")


def _print_table(history):
    print(f"\n  {'Mo':>5}  {'Period':>13}  {'COI':>18}  {'Cash':>15}  {'Total Assets':>18}  {'Passive/mo':>15}  FIRE?")
    print("  " + "-" * 94)
    for h in history:
        flag = " <-- FIRE" if h["fire"] else ""
        print(f"  {h['month']:>5}  {_yr_mo(h['month']):>13}  {_fmt(h['coi']):>18}  "
              f"{_fmt(h['cash']):>15}  {_fmt(h['total_assets']):>18}  "
              f"{_fmt(h['passive_income_mo']):>15}  {flag}")


def _header(title):
    print("=" * 65)
    print(f"  {title}")
    print("=" * 65)
    annual_exp  = 12 * MONTHLY_EXPENDITURE
    fire_target = annual_exp / 0.04
    print(f"  Monthly expenditure : {_fmt(MONTHLY_EXPENDITURE)}")
    print(f"  Annual expenditure  : {_fmt(annual_exp)}")
    print(f"  FIRE target (COI)   : {_fmt(fire_target)}  (= 25× annual expense)")
    print("=" * 65)


# ---------------------------------------------------------------------------
# Program functions
# ---------------------------------------------------------------------------

def fn1_estimate_fire(max_years=200):
    """
    Function 1 — Estimate current Total Assets and months/years to FIRE.
    Runs automatically when the script is executed.
    """
    log_path = os.path.join(OUTPUT_DIR, "fn1_log.txt")
    _header("fn1 — Estimate Time to FIRE")

    with open(log_path, "w", encoding="utf-8") as log_file:
        coi            = INITIAL_COI
        remaining_cash = INITIAL_CASH
        history        = []

        for month in range(1, max_years * 12 + 1):
            _log_month(month, coi, remaining_cash, MONTHLY_SALARY, log_file)
            coi, remaining_cash, total_assets = _compute_month(coi, remaining_cash)
            history.append({
                "month":             month,
                "coi":               coi,
                "cash":              remaining_cash,
                "total_assets":      total_assets,
                "passive_income_mo": 0.04 * coi / 12,
                "fire":              _fire_achieved(coi),
            })
            if _fire_achieved(coi):
                print(f"\n  FIRE achieved in {_fire_duration(month)}.")
                print(f"  Final COI           : {_fmt(coi)}")
                print(f"  Total Assets        : {_fmt(total_assets)}")
                print(f"  Passive income/mo   : {_fmt(0.04 * coi / 12)}")
                print(f"\n  Calculation log     : {log_path}")
                _print_table(history)
                return history

        print(f"\n  FIRE not achievable within {max_years} years at current parameters.")
        print(f"  Total Assets after {max_years} years: {_fmt(history[-1]['total_assets'])}")
        print(f"\n  Calculation log     : {log_path}")
        _print_table(history)
        return history



def fn2_reestimate_with_events(events, max_years=200):
    """
    Function 2 — Re-estimate Total Assets given UE/UI events.

    Args:
        events: list of (month, ue, ui)
                e.g. [(3, 5000, 0), (7, 0, 10000)]
                     month 3 → unexpected expense 5,000
                     month 7 → unexpected income  10,000
    """
    log_path = os.path.join(OUTPUT_DIR, "fn2_log.txt")
    _header("fn2 — Re-estimate with Unexpected Expenditure / Income")

    print("\n  Registered events:")
    for mo, ue, ui in sorted(events, key=lambda e: e[0]):
        print(f"    {_yr_mo(mo)} (month {mo}) — UE: {_fmt(ue)}   UI: {_fmt(ui)}")

    with open(log_path, "w", encoding="utf-8") as log_file:
        event_map      = {e[0]: (e[1], e[2]) for e in events}
        coi            = INITIAL_COI
        remaining_cash = INITIAL_CASH
        history        = []

        for month in range(1, max_years * 12 + 1):
            ue, ui = event_map.get(month, (0, 0))
            _log_month(month, coi, remaining_cash, MONTHLY_SALARY, log_file, ue=ue, ui=ui)
            coi, remaining_cash, total_assets = _compute_month(coi, remaining_cash, ue=ue, ui=ui)
            history.append({
                "month":             month,
                "coi":               coi,
                "cash":              remaining_cash,
                "total_assets":      total_assets,
                "passive_income_mo": 0.04 * coi / 12,
                "ue":                ue,
                "ui":                ui,
                "fire":              _fire_achieved(coi),
            })
            if _fire_achieved(coi):
                break

    fire_month = next((h["month"] for h in history if h["fire"]), None)
    if fire_month:
        h = history[fire_month - 1]
        print(f"\n  FIRE achieved in {_fire_duration(fire_month)} with events applied.")
        print(f"  Final COI           : {_fmt(h['coi'])}")
        print(f"  Total Assets        : {_fmt(h['total_assets'])}")
        print(f"  Passive income/mo   : {_fmt(h['passive_income_mo'])}")
    else:
        print(f"\n  FIRE not achieved within {max_years} years with these events.")

    print(f"\n  Calculation log     : {log_path}")
    _print_table(history)
    return history


def _simulate_to_fire(mroi, salary, risk_tolerance, monthly_exp, max_years=200):
    """Run monthly simulation with given params; return fire month or None."""
    coi            = INITIAL_COI
    remaining_cash = INITIAL_CASH
    for month in range(1, max_years * 12 + 1):
        cash_earned    = salary * (1 - risk_tolerance)
        coi_appended   = salary * risk_tolerance
        total_cash     = remaining_cash + cash_earned
        coi            = coi * (1 + mroi) + coi_appended
        remaining_cash = total_cash - monthly_exp
        if 0.04 * coi >= 12 * monthly_exp:
            return month
    return None


def _plot_curve(x_vals, fire_years, current_x, xlabel, title, out_path,
                x_fmt=lambda v: v, x_label_fmt=lambda v: f"{v}", max_years=200):
    """Shared plotting helper for all fn3 sub-plots."""
    x_reach = [x_fmt(x) for x, y in zip(x_vals, fire_years) if y is not None]
    y_reach = [y / 12   for y     in fire_years             if y is not None]
    x_no    = [x_fmt(x) for x, y in zip(x_vals, fire_years) if y is None]

    _, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_reach, y_reach, color="steelblue", linewidth=2, marker="o", markersize=3)

    if x_no:
        ax.axvspan(x_no[0], x_no[-1], alpha=0.12, color="red",
                   label=f"Not achievable within {max_years} yr")

    # Nearest data point to current value
    step     = (x_vals[-1] - x_vals[0]) / max(len(x_vals) - 1, 1)
    curr_yr  = next((y / 12 for x, y in zip(x_vals, fire_years)
                     if abs(x - current_x) <= step and y is not None), None)
    ax.axvline(x=x_fmt(current_x), color="tomato", linestyle="--", linewidth=1.5,
               label=f"Current = {x_label_fmt(current_x)}" +
                     (f"  →  {curr_yr:.1f} yr" if curr_yr else "  →  not achievable"))

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Years to FIRE", fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.show()
    print(f"  Saved → {out_path}")


def fn3(steps=60, max_years=200):
    """
    Function 3 — Generate 4 plots showing years to FIRE as each variable changes
    while all others stay fixed at their definition-area values.

      Plot 1: AROI            (1% – 30%)
      Plot 2: Monthly Expenditure
      Plot 3: Monthly Salary
      Plot 4: Risk Tolerance Rate
    """
    _header("fn3 — Years to FIRE vs Key Variables (4 plots)")

    # ── Plot 1: AROI ────────────────────────────────────────────────────────
    print(f"\n  [1/4] Sweeping AROI...")
    aroi_vals  = [0.01 + i * (0.30 - 0.01) / (steps - 1) for i in range(steps)]
    fire_aroi  = [_simulate_to_fire((1 + a) ** (1/12) - 1, MONTHLY_SALARY,
                                     RISK_TOLERANCE, MONTHLY_EXPENDITURE, max_years)
                  for a in aroi_vals]
    _plot_curve(aroi_vals, fire_aroi, AROI,
                xlabel="AROI (%)",
                title="Years to FIRE vs Annual Return of Investment (AROI)",
                out_path=os.path.join(OUTPUT_DIR, "fn3_1_fire_vs_aroi.png"),
                x_fmt=lambda v: v * 100,
                x_label_fmt=lambda v: f"{v*100:.1f}%",
                max_years=max_years)

    # ── Plot 2: Monthly Expenditure ─────────────────────────────────────────
    print(f"\n  [2/4] Sweeping Monthly Expenditure...")
    exp_min   = MONTHLY_EXPENDITURE * 0.4
    exp_max   = MONTHLY_EXPENDITURE * 1.8
    exp_vals  = [exp_min + i * (exp_max - exp_min) / (steps - 1) for i in range(steps)]
    fire_exp  = [_simulate_to_fire(MROI, MONTHLY_SALARY, RISK_TOLERANCE, e, max_years)
                 for e in exp_vals]
    _plot_curve(exp_vals, fire_exp, MONTHLY_EXPENDITURE,
                xlabel=f"Monthly Expenditure ({CURRENCY})",
                title="Years to FIRE vs Monthly Expenditure",
                out_path=os.path.join(OUTPUT_DIR, "fn3_2_fire_vs_expenditure.png"),
                x_fmt=lambda v: v,
                x_label_fmt=lambda v: f"{v:,.0f}",
                max_years=max_years)

    # ── Plot 3: Monthly Salary ──────────────────────────────────────────────
    print(f"\n  [3/4] Sweeping Monthly Salary...")
    sal_min   = MONTHLY_SALARY * 0.3
    sal_max   = MONTHLY_SALARY * 2.5
    sal_vals  = [sal_min + i * (sal_max - sal_min) / (steps - 1) for i in range(steps)]
    fire_sal  = [_simulate_to_fire(MROI, s, RISK_TOLERANCE, MONTHLY_EXPENDITURE, max_years)
                 for s in sal_vals]
    _plot_curve(sal_vals, fire_sal, MONTHLY_SALARY,
                xlabel=f"Monthly Salary ({CURRENCY})",
                title="Years to FIRE vs Monthly Salary",
                out_path=os.path.join(OUTPUT_DIR, "fn3_3_fire_vs_salary.png"),
                x_fmt=lambda v: v,
                x_label_fmt=lambda v: f"{v:,.0f}",
                max_years=max_years)

    # ── Plot 4: Risk Tolerance Rate ─────────────────────────────────────────
    print(f"\n  [4/4] Sweeping Risk Tolerance Rate...")
    rt_vals   = [0.05 + i * (0.95 - 0.05) / (steps - 1) for i in range(steps)]
    fire_rt   = [_simulate_to_fire(MROI, MONTHLY_SALARY, r, MONTHLY_EXPENDITURE, max_years)
                 for r in rt_vals]
    _plot_curve(rt_vals, fire_rt, RISK_TOLERANCE,
                xlabel="Risk Tolerance Rate (%)",
                title="Years to FIRE vs Risk Tolerance Rate",
                out_path=os.path.join(OUTPUT_DIR, "fn3_4_fire_vs_risk_tolerance.png"),
                x_fmt=lambda v: v * 100,
                x_label_fmt=lambda v: f"{v*100:.0f}%",
                max_years=max_years)

    print("\n  All 4 plots generated.")


# ---------------------------------------------------------------------------
# Entry point — CLI parser
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FIRE Estimator")
    group  = parser.add_mutually_exclusive_group()
    group.add_argument("--fn1", action="store_true",
                       help="Estimate time to FIRE (default)")
    group.add_argument("--fn2", nargs="+", metavar="EVENT",
                       help='Re-estimate with UE/UI events (month-based), e.g. "3 5000 0" "7 0 10000"')
    group.add_argument("--fn3", action="store_true",
                       help="Generate 4 plots: years-to-FIRE vs AROI / expenditure / salary / risk tolerance")

    args = parser.parse_args()

    if args.fn2 is not None:
        events = []
        for token in args.fn2:
            mo, ue, ui = token.split()
            events.append((int(mo), float(ue), float(ui)))
        fn2_reestimate_with_events(events)
    elif args.fn3:
        fn3()
    else:
        fn1_estimate_fire()
