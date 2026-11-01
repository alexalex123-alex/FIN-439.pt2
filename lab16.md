# Lab 16 — Provenance Gate

Prepared with AI assistance using the course's fictional data. The program and checks below were
actually run. Self-review replaces the partner activity under the student's reported accommodation
for missed sessions while on military orders; no partner participation is claimed. Lab 17 is excluded.

## Define

The decision is whether a price was available when a simulated trade would have been made.
The cutoff is March 31, 2026. Information first published later cannot support that decision,
even if its observation month falls before the cutoff.

## Represent: two different clocks

The observation month describes the period measured; publication time describes when the value
became available. A revision changes the reported value for an existing observation month and has
its own publication date. In ALFRED-style records, `date` is the observation date and
`realtime_start` identifies the start of the vintage's availability. A monthly label alone cannot
establish what a historical investor could have seen.

For AAA's February price, the March 10 publication reports 104; a March 25 publication revises it
to 103. Both concern February, but only the revised 103 belongs in the March 31 panel.

## Implement: asof.py

Editable inputs are `TABLE` and `DECISION_DATE` at the top. No external packages or API credentials
are required. Source row numbers survive every stage so exclusions remain traceable.

The program first isolates missing tickers and removes duplicated data records. Its duplicate key
omits the row number: otherwise an identical observation on another numbered row would escape
deduplication. Next it excludes publications beyond the cutoff and then selects the newest remaining
vintage for each ticker/month. Applying the cutoff before selecting revisions prevents later
revisions from overwriting the values a historical investor actually knew.

`signals` calculates `(latest price / previous calendar month's price - 1) × 100`.
It reports N/A if an adjacent month is missing, rather than mislabelling a multi-month change.
The naive comparison uses the same missing-ticker and duplicate cleanup but ignores the publication
cutoff and chooses each month's latest vintage. It demonstrates hindsight contamination.

## Validate: actual output

| Stage | Excluded row IDs | Count |
|---|---|---:|
| Missing ticker | 11 | 1 |
| Exact duplicate | 7 | 1 |
| Publication after cutoff | 3, 8, 10 | 3 |
| Earlier vintage replaced | 2 | 1 |
| Retained panel | 1, 4, 5, 6, 9, 12 | 6 |

| Fund | March 31 as-of signal | Naive signal |
|---|---|---|
| AAA | +1.98%, February | +5.83%, March |
| BBB | −1.02%, February | −5.15%, March |
| CCC | +0.91%, February | +1.82%, February revised |

Example calculation: AAA's as-of change is `(103 / 101 - 1) × 100 = 1.980198...%`.
Its naive change instead uses `(109 / 103 - 1) × 100 = 5.825242...%`.
These compare different months; the gap is not merely a revision to the same return.

Every input row is accounted for exactly once in the funnel or final panel. Additional tests cover
same-day publication inclusion, a cutoff before a revision, missing adjacent months, and conflicting
prices with identical publication dates. Conflicting same-date values are refused rather than
resolved by an arbitrary guess. `output.txt` contains the real console runs; `validation.txt` records
the verification checks. The source inputs retain the March 31 cutoff.

## Separate sanity review: worked arithmetic

For the exercise's one-year zero-coupon instruments, yield is `(100 / price - 1) × 100`.
The following are AI-assisted worked calculations for the student to reproduce by hand; they are
not a claim that the student's required hand calculation has already occurred.

| Row | Calculation | Yield | Classroom finding |
|---|---|---:|---|
| 1 | (100 / 101 − 1) × 100 | −0.99% | Negative yield |
| 4 | (100 / 103 − 1) × 100 | −2.91% | Negative yield |
| 5 | (100 / 98 − 1) × 100 | +2.04% | No specified flag |
| 6 | (100 / 97 − 1) × 100 | +3.09% | No specified flag |
| 9 | (100 / 110 − 1) × 100 | −9.09% | Negative yield; riskier CCC priced above AAA and BBB |
| 12 | (100 / 111 − 1) × 100 | −9.91% | Negative yield; riskier CCC priced above AAA and BBB |

All six pass the timing rules, but four trigger the exercise's plausibility checks. The program prints
this separate review without changing the required provenance panel or its reference signals.
Negative yields are a classroom warning here, not mathematically impossible in real markets;
credit comparisons also require otherwise comparable instruments. The planted-data exercise supplies
the one-year maturity and simplified expected credit ordering.

## Self-review: later-date attack

I ran the program with a cutoff of April 15, 2026. This admits the April releases, after which the
as-of results equal the naive results: AAA +5.83%, BBB −5.15%, CCC +1.82%. In CCC's case, the
April 5 release replaces the earlier February vintage; AAA and BBB gain March observations.
The test used a command-line override, leaving the saved March 31 default unchanged.


## Explain the revision code

In `latest_vintages`, `key = (record.ticker, record.month)` identifies the economic observation.
`previous = latest.get(key)` retrieves its current candidate. If there is no candidate, or the new
publication is later, `latest[key] = record` stores the new winner. The input to this function in
the as-of path has already passed the publication cutoff, so its winner is the latest **knowable**
publication, not the latest publication visible today.

**Personal comprehension response (student's own words):** "do 103 because it is more recent"

**Feedback:** Correct. The revision to 103 was published on March 25, before the March 31 cutoff,
so it is the latest available value. A more recent revision published after the cutoff would not qualify.

## Learn and reflect

Look-ahead bias occurs when a historical decision uses information unavailable at that time. A
backtest can inadvertently gain that information by joining on observation dates while ignoring
release dates, or by replacing historical values with today's revised series.

1. **Which exclusion mattered most?** For AAA's apparent opportunity, rule 3 matters most: it
   excludes row 3, whose March value was only released in April. Rule 4 still matters because it
   replaces row 2 with the revision available by March 31. There is no single universally dominant
   rule: the answer depends on the ticker and decision being evaluated.
2. **What would the naive backtest claim?** It would show AAA's +5.83% March price rise as if it
   were observable by March 31, although that price was released April 10. It would also use
   BBB's later March decline and CCC's later revision. This does not prove a particular strategy's
   profit; it proves the inputs include information the historical decision could not use.
3. **What fifth rule catches the flagged rows?** In this training setting, quarantine one-year
   zero-coupon prices above face value and check same-month credit-price ordering. The price-above-100
   condition alone identifies rows 1, 4, 9 and 12; the ordering check supplies an additional reason
   to question CCC. Keep a separate audit trail rather than silently changing prices.

A fixed publication lag is weaker than explicit as-of filtering: different releases arrive at
different times and revisions can arrive much later. The correct control uses each record's actual
availability date and the vintage known at the decision cutoff.

## Personal completion checklist

- [x] Answer the comprehension question in your own words; student response recorded above.
- [ x] Run `asof.py`, then the April 15 probe, and review the output.
- [ x] Reproduce the yield calculations by hand and explain observation time versus publication time.
- [ x] Review the reflection and confirm it represents your understanding.
- [ x] Complete the assigned ALFRED reading or the course handout alternative.
- [ x] Upload the files to GitHub and submit their links through Lab 16 in Brightspace.

## Source

[Course Lab 16 — Provenance Gate](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md)
provides the fictional observations, required filter and reference results. No market data were fetched
for this exercise. No claim is made that personal study, attendance or submission was completed by AI.
