"""Lab 14: Meridian training inputs. All rates and weights are decimals.

Run: python portfolio.py
Uses only the Python standard library; functions can be imported by Lab 15.
"""
import math

ASSETS = (
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005, "reserve": True},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.07, "reserve": True},
    {"name": "Investment-grade bond fund", "return": 0.05, "volatility": 0.06, "reserve": False},
    {"name": "Global equity index fund", "return": 0.08, "volatility": 0.16, "reserve": False},
)
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
CPI_ESTIMATE = 0.025
REAL_RETURN_TARGET = 0.04
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_TARGET
BENCHMARK_WEIGHTS = [0.0, 0.0, 0.4, 0.6]


def validate_inputs(assets, correlations):
    n = len(assets)
    if n == 0 or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square and match the assets.")
    for asset in assets:
        if not math.isfinite(asset["return"]):
            raise ValueError("Expected returns must be finite.")
        if not math.isfinite(asset["volatility"]) or asset["volatility"] <= 0:
            raise ValueError("Volatilities must be finite and positive for inverse volatility.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i}][{j}] must be between -1 and 1.")
            if not math.isclose(value, correlations[j][i], abs_tol=1e-12):
                raise ValueError(f"Correlation table must be symmetric: [{i}][{j}].")
        if not math.isclose(correlations[i][i], 1.0, abs_tol=1e-12):
            raise ValueError("Each asset's correlation with itself must equal 1.")


def covariance_matrix(assets, correlations):
    validate_inputs(assets, correlations)
    return [[correlations[i][j] * assets[i]["volatility"] * assets[j]["volatility"]
             for j in range(len(assets))] for i in range(len(assets))]


def validate_weights(weights, count):
    if len(weights) != count or any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError("Provide one finite, nonnegative weight per asset.")
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-10):
        raise ValueError("Weights must sum to 1.")


def equal_weights(assets):
    return [1 / len(assets)] * len(assets)


def inverse_volatility_weights(assets):
    inverse = [1 / asset["volatility"] for asset in assets]
    return [value / sum(inverse) for value in inverse]


def expected_return(weights, assets):
    validate_weights(weights, len(assets))
    return sum(w * asset["return"] for w, asset in zip(weights, assets))


def portfolio_volatility(weights, covariance):
    validate_weights(weights, len(covariance))
    # Both (i, j) and (j, i) occur: cross-asset covariance is counted twice.
    variance = sum(weights[i] * weights[j] * covariance[i][j]
                   for i in range(len(weights)) for j in range(len(weights)))
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance; review the correlation inputs.")
    return math.sqrt(max(0.0, variance))


def reserve_weight(weights, assets):
    validate_weights(weights, len(assets))
    return sum(w for w, asset in zip(weights, assets) if asset["reserve"])


def meets_objective(result, objective):
    return result >= objective or math.isclose(result, objective, abs_tol=1e-12)


def main():
    try:
        covariance = covariance_matrix(ASSETS, CORRELATIONS)
        portfolios = {"Benchmark": BENCHMARK_WEIGHTS,
                      "Equal weight": equal_weights(ASSETS),
                      "Inverse volatility": inverse_volatility_weights(ASSETS)}
        print("Meridian: course-authored training values, not market forecasts")
        print(f"Objective: {OBJECTIVE_RETURN:.2%} (CPI estimate {CPI_ESTIMATE:.1%} + {REAL_RETURN_TARGET:.1%})")
        for name, weights in portfolios.items():
            result = expected_return(weights, ASSETS)
            print(f"\n{name}")
            for asset, weight in zip(ASSETS, weights):
                print(f"  {asset['name']}: {weight:.1%}")
            print(f"  Expected return: {result:.2%}")
            print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
            print(f"  Reserve-eligible: {reserve_weight(weights, ASSETS):.1%}")
            print(f"  Meets objective: {'yes' if meets_objective(result, OBJECTIVE_RETURN) else 'no'}")
    except ValueError as error:
        raise SystemExit(f"Cannot run: {error}") from error


if __name__ == "__main__":
    main()
