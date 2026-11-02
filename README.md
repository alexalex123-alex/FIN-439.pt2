# FIN43900 — Labs 14–17

This combined guide covers the portfolio and point-in-time data labs in numerical order.
Individual Markdown reports contain the full calculations, explanations and completion checklists.

## Repository organization

Keep this README at the repository root. Keep each lab's deliverables in its own folder:

```text
README.md                 <- this combined guide
lab14/
    portfolio.py
    mandate.py
    lab14.md
    validation.txt
lab15/
    portfolio.py
    app.py
    prices.csv
    lab15.md
    requirements.txt
    validation.txt
    README.md             <- optional lab-specific guide
lab16/
    asof.py
    lab16.md
    output.txt
    validation.txt
    README.md             <- optional lab-specific guide
lab17/
    asof_app.py
    asof_data.py
    lab17.md
    audit_results.json
    validation.txt
    requirements.txt
    README.md             <- optional lab-specific guide
```

Uploading a file with the same name to the same folder updates that file. A README inside `lab16/`
is separate from one inside `lab17/`. The same protection matters for the two versions of
`portfolio.py` and each lab's `validation.txt`. Do not combine all lab files into the root folder.
Prior committed versions can normally be recovered from GitHub's file/commit history.

This is the intended layout, not a claim that these folders have already been created on GitHub.
If files were uploaded at the root, organize the correct lab versions into these folders first.
Preserve any existing Lab 13 files and other research materials in the repository.

## Setup

Labs 14 and 16 use Python's standard library. Labs 15 and 17 require Streamlit; Lab 17 also needs
internet access for public FRED/ALFRED downloads. No FRED API key or account is needed.

For either Streamlit lab, open a terminal inside its folder and run the following on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If the `python` command does not work, substitute the path to an installed Python executable.
Do not upload `.venv` or `__pycache__`. Press Ctrl+C in the terminal to stop an app.

## Lab 14 — Portfolio Baselines

**Goal:** calculate three Meridian training portfolios and test the benchmark against its mandate.

| File | Purpose |
|---|---|
| `portfolio.py` | Covariance, expected return, volatility, reserve weight and baseline allocations |
| `mandate.py` | Original Lab 13 checker with candidates A–D preserved and benchmark E added |
| `lab14.md` | Results, calculation explanation, discussion and personal checklist |
| `validation.txt` | Verification record |

Run inside `lab14/`:

```powershell
python portfolio.py
python mandate.py
```

| Portfolio | Return | Volatility | Reserve |
|---|---:|---:|---:|
| Benchmark | 6.80% | 10.46% | 0.0% |
| Equal weight | 5.20% | 5.21% | 50.0% |
| Inverse volatility | 3.77% | 1.05% | 90.3% |

The benchmark clears the 6.5% return target but fails the 3% reserve requirement.
Changing both IG–equity correlation entries to 0.50 produces 11.00% benchmark volatility.
Restore 0.25 after the probe. Invalid and asymmetric correlations are rejected.

## Lab 15 — Portfolio Stability Decision

**Goal:** turn the portfolio engine into a Streamlit app and test allocation sensitivity.

| File | Purpose |
|---|---|
| `portfolio.py` | Extended Lab 15 engine, including CSV estimates and 5-point allocation search |
| `app.py` | Interactive portfolio app |
| `prices.csv` | BIL, IEF, LQD and VT adjusted month-end prices |
| `lab15.md` | Mandate, sources, flowchart, validation, self-review and proposed pilot decision |
| `requirements.txt` | Tested dependency version |
| `validation.txt` | Verification record |
| `README.md` | Optional detailed lab-specific walkthrough |

Run inside `lab15/` after setup:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

1. Meridian starts at a 6.5% target and 3% reserve minimum; expect weights 0/20/25/55.
2. Lower equity's return from 8% to 7%; expect 0/10/10/80 and a 25-percentage-point change.
3. Choose Northbridge: target 5.5%, reserve minimum 3%, only BIL reserve-eligible.
4. Upload `prices.csv`; compare all months with the last 36 months.

Saved Northbridge results use the November 1, 2026 download:

| Run | BIL / IEF / LQD / VT (%) | Return estimate | Volatility |
|---|---|---:|---:|
| All 60 months | 70 / 0 / 0 / 30 | 5.73% | 4.55% |
| Last 36 months | 90 / 0 / 0 / 10 | 5.97% | 1.21% |
| VT estimate reduced one percentage point | 65 / 0 / 0 / 35 | 5.73% | 5.28% |

Returns are historical estimates, not guarantees. This static app does not verify the full turnover,
spending or implementation requirements of the client's mandate.

## Lab 16 — Provenance Gate

**Goal:** establish which fictional observations were knowable on March 31, 2026.

| File | Purpose |
|---|---|
| `asof.py` | Four-rule point-in-time filter, signals and separate sanity review |
| `lab16.md` | Concepts, worked yields, self-review, reflection and recorded comprehension answer |
| `output.txt` | Actual March 31 and April 15 console output |
| `validation.txt` | Verification record |
| `README.md` | Optional detailed run guide |

Run inside `lab16/`:

```powershell
python asof.py
python asof.py --decision-date 2026-04-15
```

The gate handles missing tickers, exact duplicates, late publications and superseded vintages,
in that order. Retained March 31 row IDs are 1, 4, 5, 6, 9 and 12.

| Fund | March 31 as-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% | +5.83% |
| BBB | −1.02% | −5.15% |
| CCC | +0.91% | +1.82% |

At April 15, all three as-of signals match the naive signals. The override leaves the saved default
unchanged. The separate yield review flags rows 1, 4, 9 and 12 under the exercise's assumptions.

## Lab 17 — Point-in-Time Audit

**Goal:** display live FRED series, compare historical ALFRED vintages, and assess CPIAUCSL's admission.

| File | Purpose |
|---|---|
| `asof_app.py` | Streamlit charts, date controls and comparison table |
| `asof_data.py` | Required cached download, parsing and comparison functions |
| `lab17.md` | CPIAUCSL data card, evidence, self-review and proposed quarantine decision |
| `audit_results.json` | Saved computed results, URLs and retrieval timestamps |
| `validation.txt` | Verification record |
| `requirements.txt` | Tested dependency version |
| `README.md` | Optional detailed run guide |

Run inside `lab17/` after setup:

```powershell
.\.venv\Scripts\python.exe -m streamlit run asof_app.py
```

1. Four rates are selected initially. Set **As known on** to October 5, 2026:

   | Series | Last observation known then | Value |
   |---|---|---:|
   | BAA | September 2026 | 6.47 |
   | FEDFUNDS | September 2026 | 3.75 |
   | DGS10 | October 2, 2026 | 5.28 |
   | MORTGAGE30US | October 1, 2026 | 7.28 |

2. Add **PAYEMS** and set January 15, 2025. December 2024 reads 159,536 in that vintage;
   the November 1, 2026 download reports 158,316 for that same observation, with 59 revised shared
   dates in the selected window.
3. Replace the extra ID with **CPIAUCSL**. Compare October 31 and November 1, 2026; the saved audit
   shows September 2026 at 336.298 on both dates.
4. Use October 5, 2026 to see CPI's lag and January 15, 2025 to see historical revisions.

Charts show current histories; the table performs the point-in-time comparison. CPIAUCSL is a
seasonally adjusted index, not a percent inflation rate. Live results can change after future
releases. Unknown series or unavailable vintages display an error rather than fabricated data.

## Review and submission

The labs were prepared with AI assistance. Self-review is labelled where it replaces partner work
under the student's reported accommodation. Personal checks and explanations remain the student's
responsibility; mark only completed items in each lab report.

For Lab 17, personally confirm the three CPI values listed in `lab17.md` on its linked FRED page.
Review each proposed decision and explanation before submission. Upload the correct files to the
matching lab folder, then submit the requested direct GitHub file links through the corresponding
Brightspace checkout. If previously submitted links change when files are moved, update those links.

This guide does not certify upload or Brightspace submission status.
