"""Meridian mandate checker. Run with: python mandate.py"""

# Editable inputs: monetary amounts are USD millions; weights are percentages.
HOLDINGS = {
    "Cash": ("none", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}
# Weights follow the holdings order above.
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
    # Lab 14 benchmark: 60% global equity, 40% investment-grade bonds.
    "E": [0, 0, 0, 60, 40, 0, 0, 0],
}
RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}
TOLERANCE = 1e-9


def check(weights):
    """Return measured values and outcomes for the five checkable rules."""
    if len(weights) != len(HOLDINGS):
        raise ValueError("Supply exactly one weight per holding.")
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    reserve_weight = 0
    liquid_weight = 0
    company_weights = {}
    for (issuer, days, reserve_eligible), weight in zip(HOLDINGS.values(), weights):
        if reserve_eligible:
            reserve_weight += weight
        if days <= LIQUIDITY_WINDOW:
            liquid_weight += weight
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    total = sum(weights)
    lowest = min(weights)
    largest_company = max(company_weights.values(), default=0)
    return [
        ("Weights sum to 100", total, abs(total - 100) <= TOLERANCE),
        ("Long-only (lowest weight)", lowest, lowest >= -TOLERANCE),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight,
         reserve_weight >= reserve_minimum - TOLERANCE),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE}%",
         liquid_weight, liquid_weight >= MINIMUM_LIQUID_SHARE - TOLERANCE),
        (f"Largest single company <= {ISSUER_LIMIT}%", largest_company,
         largest_company <= ISSUER_LIMIT + TOLERANCE),
    ]


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        results = check(weights)
        for label, value, passed in results:
            print(f"  {label}: {value:.1f} {'pass' if passed else 'FAIL'}")
        print("  Calendar-year loss: requires CIO clarification")
        failures = sum(not passed for _, _, passed in results)
        print("  passes every checkable rule" if failures == 0
              else f"  fails {failures} rule(s)")


if __name__ == "__main__":
    main()
