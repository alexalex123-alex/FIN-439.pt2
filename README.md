# Lab 19 — Legend Panel

Built with Codex AI assistance. Alex must review the analysis and proposed decision; education, not investment advice.

**Start with `LAB19.md`** for the results, bull/bear drafts, proposed decision and remaining student activities.

## Run the app

Open PowerShell in this folder and run:

```powershell
.\run.ps1
```

The launcher finds Python, installs dependencies if necessary and opens Streamlit. Alternatively:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Saved SEC runs for **COST, NVDA and JPM** work offline. Enter the ticker in the sidebar. Each view shows the panel table, three editable memos and verdicts side by side, a guard across all memos, the original Lab 18 chart/table and source evidence. Set Wood's growth threshold to 5 for the COST probe, then restore 15. The app warns that a changed evidence set or threshold requires reviewing saved memos.

## Reproduce the calculations

From this folder, with any working Python:

```powershell
python .agents/skills/legend-panel/scripts/panel.py COST --facts reports/raw/COST_companyfacts.json --validate-memos
python .agents/skills/legend-panel/scripts/panel.py NVDA --facts reports/raw/NVDA_companyfacts.json --validate-memos
python .agents/skills/legend-panel/scripts/panel.py COST --facts reports/raw/COST_companyfacts.json --growth-threshold 5 --out reports/probe
python -m pytest tests -q
```

Tests require pytest in addition to the app requirements. Financial calculations use the standard library. Live downloads omit `--facts` and require `SEC_USER_AGENT` with your name and email; the app also has a masked contact field. The contact is not saved. Snapshots have SHA-256 sidecars; every financial input retains its tag, period, filing date and accession. Filing cutoff is November 5, 2026. Flows must have matching annual periods, and only 10-K observations are eligible. Latest eligible filing wins within each permitted tag, preserving Lab 18's tag priority.

Open this folder as your Codex project to discover `.agents/skills/`. Ask: “Use $legend-panel on NVDA; apply each investor skill separately to the printed evidence and validate every memo.” The new Wood and Burry skills use shared code to ensure all investors see the same facts. The app displays AI-authored Markdown; it does not make live model calls. A refreshed report requires new memo review. Number flags check token support, not the truth of qualitative claims or whether a supported number was used correctly.

## Files to review and upload

| File or folder | Purpose |
|---|---|
| `LAB19.md` | Concise lab write-up and remaining student work |
| `app.py`, `run.ps1`, `requirements.txt` | Runnable app |
| `.agents/skills/` | Buffett, Wood, Burry and panel workflows; bundled calculation scripts |
| `reports/COST_panel.md`, `reports/NVDA_panel.md` | Printed evidence and checks |
| `reports/*_buffett_memo.md`, `*_cathie_wood_memo.md`, `*_burry_memo.md` | Separate AI-authored memos |
| `reports/probe/` | COST threshold experiment |
| `reports/raw/` | Reproducible SEC snapshots and provenance |
| `reference/VT_selection.json` | Dated Vanguard selection evidence |
| `VALIDATION.md`, `tests/` | Verification record and repeatable checks |
| `PROJECT2_NEXT.md` | How earlier labs connect to Project 2 |
| `lab18-records/` | Tuesday's original documentation, preserved as history |

Upload the entire folder, including hidden `.agents`, to a `Lab19` folder in your course GitHub repository. Use Git or enable hidden files in Explorer; a browser folder upload can omit dotfolders. Do not upload `.venv`, caches or contact details. Submit GitHub links through **Brightspace → Quizzes → Lab 19**. The enforced closing time is in Brightspace; no submission is claimed here.

## Sources

[Lab 19](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md), [session slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/slides-session-19.md), [SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [Vanguard VT](https://investor.vanguard.com/investment-products/etfs/profile/vt#portfolio-composition), and FAskills investor pages linked in each skill. FAskills was read as a reference, not installed.
