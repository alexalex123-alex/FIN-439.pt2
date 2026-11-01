# Lab 14 — Portfolio Baselines

Status: computational work verified; student and partner activities remain to be completed.
Built with AI assistance. Inputs are fictional course training values, not market estimates.

## Question and results

Which baseline clears the return target, and what happens when the mandate is checked?
CPI is assumed to be 2.5%; adding 4% gives a 6.5% return target.

| Portfolio | Bills / 10-year / IG / equity (%) | Return | Volatility | Reserve share | Return target met? |
|---|---|---|---|---|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

Displayed inverse-volatility weights total 99.9% because of rounding; unrounded weights total 100%.
The reserve share uses unrounded weights too.

The benchmark clears the return hurdle but holds no eligible reserve assets. The checker computes
the required reserve as 4 × $0.75 million / $100 million = 3%. Candidate E therefore fails that
rule. Neither other baseline reaches the return objective. No baseline satisfies both tests.

## Calculation walkthrough

All inputs in `portfolio.py` use decimals: 0.06 means 6%, and a weight of 0.4 means 40%.

1. `covariance_matrix` multiplies each correlation by the two assets' volatilities.
2. `expected_return` adds each weight times its asset's expected return.
3. `portfolio_volatility` sums every weighted covariance and takes the square root.
4. `reserve_weight` adds weights only where the asset's reserve flag is true.
5. `inverse_volatility_weights` computes reciprocal volatilities, then normalizes their sum.

For the benchmark, bond-equity covariance is 0.25 × 0.06 × 0.16 = 0.0024.
Its variance is (0.4² × 0.06²) + (0.6² × 0.16²) + (2 × 0.4 × 0.6 × 0.0024)
= 0.010944. The square root is approximately 0.1046136, or 10.46%.
The double loop in the code includes both bond-equity and equity-bond terms, producing the factor 2.

## Validation actually performed

See `validation.txt` for the run record. Automated checks confirmed:

- All baseline returns, volatilities and reserve shares match the reference.
- Raising the bond-equity correlation to 0.50 in both positions produces 11.00% benchmark volatility.
- An entry of 1.3 is rejected; an asymmetric matrix is also rejected.
- Your original checker still matches A-C, preserves D (100% cash), and E fails only the reserve check.
- Probes operated on copies; the saved correlation remains 0.25.

These checks were performed by the AI assistant. They do not constitute a partner swap.

## Discussion notes — review and explain in your own words

Correlations below +1 reduce the covariance contribution relative to perfectly synchronized
asset movements. Diversification can reduce portfolio volatility; it does not guarantee a profit.

Inverse-volatility weighting concentrates in bills because their 0.5% volatility gives the
largest reciprocal. This method ignores the return target, explaining its low expected return.
This method favors less volatile assets, so it puts most of the weight in Treasury bills. However, it ignores correlations and the return target, so it does not necessarily find the lowest-risk portfolio.

A possible opening for the CIO discussion is the benchmark: its return clears the hurdle, yet
its reserve allocation exposes an inconsistency between the benchmark and the mandate. It is
a useful comparison, not an allocation to adopt without changes.

## Finish personally before submission

- [ ] Explain the benchmark variance calculation to your partner without AI.
- [ ] Read the volatility function line by line and answer your partner's question.
- [ ] Ask AI to quiz you on a line you find difficult; answer before requesting an explanation.
- [ ] Run your partner's engine, perform the invalid-correlation probe, and restore the inputs.
- [ ] Discuss why the inverse-volatility allocation is concentrated and choose which baseline you would present first.
- [x] Added E to your original Lab 13 checker, retaining A-D and the original checking logic. Source: [your original mandate.py](https://github.com/alexalex123-alex/AAPL--research/blob/5882f80b9f7b2729a0c32380ba67d4cf9319000c/mandate.py).
- [ ] Upload your files to your GitHub repository and submit their links through the course checkout.



## Running the files

In a terminal opened in this folder:

```powershell
python portfolio.py
python mandate.py
```

The default Python alias was inaccessible on the assistant's run. This installed interpreter worked:

```powershell
& 'C:\Users\alxsc\AppData\Local\Python\pythoncore-3.14-64\python.exe' portfolio.py
& 'C:\Users\alxsc\AppData\Local\Python\pythoncore-3.14-64\python.exe' mandate.py
```

`portfolio.py` uses decimal weights; `mandate.py` uses percentage weights. Their holding order differs;
candidate E is explicitly mapped to 60% equity and 40% IG bonds in the checker.

## Scope

This package covers the Lab 14 checkout only.

## Sources

- [Lab 14](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md)
- [Week 9 handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md)
- [Lab 13 checker specification](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md)
