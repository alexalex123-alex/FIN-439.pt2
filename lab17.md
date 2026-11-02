# Lab 17 — Point-in-Time Audit

Prepared with AI assistance. Live downloads and automated app checks were performed November 1,
2026. The student selected CPIAUCSL for Project 2. Under the student's reported professor-approved
accommodation for military orders, the partner exercise is recorded as AI-assisted self-review.
No claim is made that an in-person partner, personal reading or manual student checks occurred.

## Define: why this series matters

Northbridge Community Scholarship Fund's draft mandate targets CPI + 3%. Consumer prices therefore
matter both to the real-return hurdle and to scholarship purchasing power. Inflation conditions may
also influence the interest-rate environment affecting BIL, IEF and LQD, and equity valuations in VT;
this is an economic rationale for investigation, not proof of predictive power.

The question is whether each input was available when an allocation decision would have been made.
This app audits timing and revisions. It does not modify Lab 15's allocations or silently replace its
agreed 2.5% inflation assumption with an observed inflation figure.

## Implement: live FRED-style app

`asof_app.py` is the Streamlit interface. `asof_data.py` holds the two cached download functions,
CSV parser and date-aligned comparisons. Both files must be kept together.

Each selected series receives one FRED request for its current history and one ALFRED request for
the requested vintage; no API key is required. A one-hour cache reduces repeat requests, while the
download-day argument prevents yesterday's cache from being reused overnight. A refresh button
clears both caches. Actual retrieval times and returned vintage-column labels are displayed.

The app opens with BAA, FEDFUNDS, DGS10 and MORTGAGE30US selected; start date is January 1, 2020,
and the cutoff defaults to the current date in America/Indianapolis. A text field adds CPIAUCSL,
PAYEMS or another FRED ID. Current-history charts are separate, preserving their own frequencies
and native units. The comparison table shows each series' latest observation then and now, the
number of later observations, and revisions on shared dates. Series IDs link to FRED.

The start date restricts the comparison window as well as the chart. Numeric blanks and dots are
missing observations: they are not replaced with zero or forward-filled. Revised count is the count
of shared, nonmissing observation dates with differing values, using a 1e-9 absolute tolerance.
A bad series displays an error while other series continue; a missing old vintage is also reported.

ALFRED sometimes returns a column labelled with an effective vintage before the requested date.
The parser accepts it only if it belongs to the correct series and is no later than the cutoff;
it also rejects observations dated after that cutoff. A vintage snapshot does not independently
certify the original intraday release time of every observation.

## Validate: October 5, 2026 reference case

These values came from the actual ALFRED downloads and were also reproduced through the app.
Comparison counts use January 1, 2020 through the latest available observation on November 1, 2026.

| Series | Last observation known October 5 | Value then | Later observations today | Revised shared observations |
|---|---|---:|---:|---:|
| BAA | September 2026 | 6.47 | 0 | 0 |
| FEDFUNDS | September 2026 | 3.75 | 0 | 0 |
| DGS10 | October 2, 2026 | 5.28 | 18 | 0 |
| MORTGAGE30US | October 1, 2026 | 7.28 | 4 | 0 |

The daily market rate has a short availability gap and no revisions in this comparison. Its last
available current observation is October 29, not automatically the current calendar date.

## Validate: PAYEMS revision probe

At a January 15, 2025 vintage, the latest PAYEMS observation is December 2024 at **159,536 thousand
persons**. Today's value for that same December 2024 observation is **158,316**, a downward change
of 1,220 thousand. The selected window contains **59 revised shared observations** and **21 later
observations**. The app reproduces the vintage value and nonzero revision count.

Do not confuse today's latest PAYEMS value (for a different month) with today's value of December
2024. A revision must compare the same observation date across vintages.

## Data card: CPIAUCSL

| Field | Record |
|---|---|
| Series | CPIAUCSL: Consumer Price Index for All Urban Consumers, All Items in U.S. City Average |
| Original producer | U.S. Bureau of Labor Statistics (BLS) |
| Distributor and source | [FRED series page](https://fred.stlouisfed.org/series/CPIAUCSL); [ALFRED series page](https://alfred.stlouisfed.org/series?seid=CPIAUCSL) |
| Measure | Consumer price level for a basket of goods and services bought by urban consumers |
| Units | Index, 1982–1984 = 100; seasonally adjusted. It is not a percentage rate. |
| Frequency | Monthly; dates such as September 1 label the observation month, not the release date |
| Publication lag | Usually released in the following month; verify actual release dates rather than imposing a fixed lag. September 2026 was released October 14, 14 days after month-end. |
| Revisions | Seasonal adjustment can revise the previous five years when annual factors are recalculated with January data released in February. The app confirms historical differences. |
| Download date | November 1, 2026; actual timestamps and URLs are in `audit_results.json` |
| Intended use | Inflation monitoring and point-in-time research relevant to the CPI + 3% mandate |
| Missing-data rule | Preserve missing observations; do not interpolate a missing month's CPI to create a signal. The downloaded series has a blank October 2025 observation. |

Source references for metadata and release timing:
[FRED CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL),
[BLS seasonal adjustment](https://www.bls.gov/cpi/seasonal-adjustment/), and
[BLS September 2026 release](https://www.bls.gov/news.release/archives/cpi_10142026.htm).

To derive an inflation rate, compute a percentage change in the index. For example, annual inflation
uses `(index this month / index twelve months earlier - 1) × 100`, with both values taken from the
vintage available at the decision date. CPIAUCSL is seasonally adjusted; the client must specify
whether the mandate instead intends an unadjusted CPI measure before it becomes a performance rule.

### Own-series date comparison

| As known on | Latest CPI observation | Value | Later observations in today's data | Revised shared dates |
|---|---|---:|---:|---:|
| October 31, 2026 | September 2026 | 336.298 | 0 | 0 |
| November 1, 2026 | September 2026 | 336.298 | 0 | 0 |
| October 5, 2026 (additional lag check) | August 2026 | 334.131 | 1 | 0 |
| January 15, 2025 (additional revision check) | December 2024 | 317.685 | 20 | 60 |

Nothing changes between the required month-end and today's comparison. A short unchanged interval
does not demonstrate that a series is never revised: the older vintage comparison finds 60 changes.
The October 5 view excludes September's CPI because its publication arrived later in October.

### Three page-value checks

The assistant opened the FRED page separately from the CSV download and matched these observations:

| Observation month | FRED page | Download | Match |
|---|---:|---:|---|
| July 2026 | 332.813 | 332.813 | Yes |
| August 2026 | 334.131 | 334.131 | Yes |
| September 2026 | 336.298 | 336.298 | Yes |

These are assistant checks. The assignment asks the student to read three values personally; that
confirmation remains on the checklist rather than being falsely marked complete.

## Fresh eyes: self-review

The self-review challenged the card's revisions field: a zero count between October 31 and November 1
could misleadingly suggest the series is never revised. The test used the older January 15, 2025
vintage and checked the BLS revision policy.

Two-sentence response: A zero count over the one-day comparison does not establish that CPIAUCSL is
unrevised, because the app finds 60 revised shared dates when comparing the January 15, 2025 vintage
with today's series. BLS describes annual recalculation of seasonal factors affecting the preceding
five years, so a historical test must retrieve the appropriate vintage instead of assuming today's
adjusted history was known then.

## Explain the vintage-download function

`download_vintage` validates the series ID and converts the cutoff into a date. It constructs the
ALFRED URL with `id` and `vintage_date`, downloads once, and passes the response through the CSV
validation described above. Its cache key includes the series, cutoff and download day, so another
date or series cannot reuse the wrong snapshot. It returns dated values with the source URL,
returned column label and actual download time.

The student requested an explanation of why today's FRED file cannot simply be trimmed to an old
date. The answer is that older observation dates in today's file may already contain later revisions;
removing newer months does not restore the original values. PAYEMS December 2024 demonstrates this:
159,536 was available in the January 2025 snapshot, while today's same-month observation is 158,316.
This is recorded as an AI-explained learning exercise, not an independent answer from the student.

## Proposed call: quarantine pending a defined as-of rule

**Quarantine CPIAUCSL from Project 2 allocation signals and historical performance evaluation for now.**
It may remain visible for exploratory monitoring, but the mandate has not specified its exact CPI
definition, and a current-vintage backtest would expose revised inputs unavailable to past decisions.

Change the call to admit when the client-approved CPI definition and transformation are documented,
every historical decision uses the ALFRED vintage available by that decision, missing values produce
no fabricated signal, and release-time handling is explicit. If intraday availability is unknown,
use the next trading session after the verified release as a conservative implementation rule and
document that choice. Do not substitute a universal fixed monthly lag for actual release/vintage data.

This call concerns the data's admission to a model, not whether CPI is economically relevant.
The app itself does not certify original release timestamps or establish predictive power.

## Learn and reflect

A data card is a compact record of provenance, definition, units, frequency, availability, revisions
and permitted use. Saying data were cleaned does not reveal when each value became available or
whether a later revision replaced the historical input. Those fields prevent information leakage
before a model consumes the series.

September's CPI was not available at September month-end, and it was still absent from the October 5
vintage. A naive backtest using today's history could therefore give a past decision access both to
unpublished months and to later-revised old months. It overstates the information set; the direction
of its effect on a particular strategy's performance is not established by this audit alone.

## Remaining student actions

- [ x] Run the app and reproduce the reference case, PAYEMS probe and CPI comparisons.
- [ x] Personally read July, August and September 2026 values on the linked FRED page and confirm the three matches above.
- [ x] Explain the vintage function without AI and restate the revision example in your own words.
- [ x] Review the proposed quarantine decision and self-review response so they reflect your understanding.
- [ x] Upload the package to GitHub and submit the direct file links in Brightspace's Lab 17 checkout.

The partner exercise is replaced with the labelled self-review above; it is not left for a partner.
Personal activities have not been marked complete on the student's behalf.

## Course and method references

- [Lab 17 assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md)
- [ALFRED help: vintages and release dates](https://alfred.stlouisfed.org/help)
- [FRED PAYEMS page](https://fred.stlouisfed.org/series/PAYEMS)

All numerical results in this report were obtained from public downloads. No reference answer is
hardcoded in the application. Live results may change after future releases or revisions; the JSON
audit preserves the results and retrieval metadata from this run. Automated verification uses
Streamlit AppTest; a manual browser review remains part of the student's walkthrough.
