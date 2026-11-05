# Lab 19 verification — November 5, 2026

**15 tests passed.** All four skill files passed the skill frontmatter validator. The app and financial checks were run with Python 3.12.14 using the working Lab 18 environment; the launcher can reuse that environment on this computer. Nothing was uploaded or submitted, at Alex's request.

| Requirement | Observed result |
|---|---|
| COST known answer | All original financial rows and rounded ROEs match the course reference; Buffett passes all checks |
| Wood COST checks | Revenue CAGR 7.51%, growth fails at 15%; R&D fact absent and check not known |
| Burry COST checks | Both pass; liabilities/equity rounds to 2.11, 1.75, 1.96, 1.64, 1.49 across the five years |
| Threshold experiment | At a 5% floor, COST growth passes and R&D remains not known; annual input rows are unchanged |
| NVIDIA run | Buffett and Wood checks pass; Burry cash-backing fails and leverage passes; three separate memos saved |
| Fund selection | Vanguard's dated VT equity holdings were ranked after grouping matching company descriptions; NVIDIA is largest at 4.52% |
| Number guard | Clean memos pass for COST, NVDA and JPM; adding 40.0% is flagged in each investor's COST memo column |
| App | COST panel, three verdicts/memos, two-series chart and annual table render through Streamlit AppTest; NVDA and JPM switches pass |
| Changed settings | Threshold probe updates the check and displays an evidence-review warning; restoring the default removes it |
| Missing data | JPM capex and owner earnings remain not found; unknown checks are preserved |
| Period rules | Quarterly and future-filed observations ignored; later eligible annual R&D observation selected |
| Edge cases | Missing inputs, incomplete windows and nonpositive ratio denominators produce unknown results |
| Provenance | Raw-snapshot SHA-256 records verified; altered snapshot/hash pair rejected |
| Download failure | Missing SEC contact produces a clear error and retains saved evidence |

Fresh SEC companyfacts were downloaded for COST, JPM and NVDA on November 5 with the caller's supplied contact header. Contact details are not included in saved files. Latest eligible 10-K facts are selected at the November 5 cutoff; the preserved original Lab 18 reports keep their explicit November 3 cutoff and were recalculated against the refreshed snapshots. All memo numbers were checked against printed evidence, with a separate semantic review by Codex. Student review remains pending.

The first verification run caught the old JPM report's snapshot hash after the raw download was refreshed. Recalculating the legacy report with its original filing cutoff corrected that mismatch. The completed run passed all 15 tests. Streamlit emitted 15 internal pandas deprecation warnings; there were no application exceptions.

The app reads saved AI-authored memos; it does not autonomously call three live models. The number guard checks numeric tokens and percentage units, not whether a supported number was assigned to the correct concept. Historical financial checks do not establish valuation, moat durability, future growth, or complete accounting quality.

No partner discussion, no-AI explanation, student-owned decision, GitHub upload or Brightspace checkout is represented as completed. See `LAB19.md` for the remaining personal activities.
