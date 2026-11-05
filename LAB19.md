# Lab 19 — Legend Panel

Built with Codex AI assistance. Code computes the evidence and checks; the memos and proposed decision below are AI-assisted drafts for Alex to review. Partner and no-AI activities are not represented as completed.

## Company selection

I continued the Northbridge scholarship-fund universe from Lab 15: BIL, IEF, LQD and VT. VT is the equity fund, and its largest company is NVIDIA (NVDA), at 4.52% in Vanguard's September 30, 2026 holdings, retrieved November 5. No substitute company was needed. This is a holding-level research exercise, not a decision to replace VT with NVIDIA.

Source: [Vanguard VT portfolio](https://investor.vanguard.com/investment-products/etfs/profile/vt#portfolio-composition); the page's [holdings data](https://investor.vanguard.com/irr/funds/profile/VT-AdditionalFundData). Selection evidence and provenance are in `reference/VT_selection.json`.

## Verified COST panel

| Investor | Computed result | Memo verdict |
|---|---|---|
| Buffett | All three checks pass | Own the business |
| Cathie Wood | Growth fails at 7.51%; R&D not known | Pass |
| Burry | Both checks pass; latest liabilities/equity 1.49 | Watch |

All five Lab 18 annual rows and the Lab 19 liabilities ratios match the independent course answers. Missing R&D is kept as not found; its ratio and check are not known. Memos are judgments, so passing checks need not produce the same verdict.

## Threshold probe

Lowering Wood's growth floor from 15% to 5% changes COST's growth check from fail to pass; R&D remains not known. The company and its 7.51% growth rate are unchanged. I retain 15% to preserve a consistent rapid-growth screen instead of choosing a cutoff to admit a preferred company. The rationale also appears under Wood's memo. Reproducible probe evidence: `reports/probe/COST_panel.md`.

## NVIDIA panel and disagreement

| Investor | Computed result | Memo verdict |
|---|---|---|
| Buffett | All three checks pass | Watch |
| Cathie Wood | Both pass: CAGR 68.30%; latest R&D/revenue 8.57% | Own the business, qualified |
| Burry | Cash-backing fails; latest liabilities/equity passes at 0.31 | Watch |

The panel agrees that NVIDIA has positive owner earnings and passes the latest liabilities/equity ceiling. Wood emphasizes rapid growth and reinvestment; Burry emphasizes income not fully backed by operating cash in several years. Buffett's numerical screen passes, but the memo withholds an ownership judgment until durability and cash conversion are better understood. A failed cash-backing check does not demonstrate manipulation.

## Bull and bear — discussion drafts

**Bull (two sentences):** NVIDIA passes Buffett's profitability and owner-earnings checks and Wood's growth and reinvestment checks, with revenue CAGR of 68.30% and latest R&D/revenue of 8.57%. Latest liabilities/equity of 0.31 also passes Burry's balance-sheet check, supporting further research into the business.

**Bear (two sentences):** NVIDIA fails Burry's requirement that operating cash flow cover net income every year; latest operating cash flow is 102,718 versus net income of 120,067, in USD millions. That gap and the limits of backward-looking growth evidence justify investigating cash conversion and profit durability before trusting a favorable ownership verdict.

## Proposed Project 2 decision — review personally

Only as a research triage tool: retain unknowns, investigate NVIDIA's cash-versus-income gap, and apply the Northbridge mandate, portfolio risk and independent valuation checks before any allocation decision.

## Learn and reflect

A panel of AI agents gives separate analytical roles the same evidence and asks each for a judgment. Here the skills are applied separately within one AI workflow; the app displays saved memos rather than running independent live models. Shared evidence and code improve consistency, but common data errors and model biases can affect every memo.

The personas disagree because they weight different questions: durable cash earnings, growth and reinvestment, or cash backing and balance-sheet skepticism. They do not provide independent confirmation simply because their names differ. The threshold experiment shows that a screen's result depends on a chosen rule; changing a rule changes classification without changing company facts.

## Finish personally

- Explain `wood_checks` in `.agents/skills/legend-panel/scripts/panel.py` line by line to your partner, without AI, including how missing inputs become not known; swap roles.
- Discuss how Wood and Burry might interpret the sell-off using their philosophies. Do not claim they actually traded today.
- Give and challenge the two-sentence bull and bear arguments with your partner; swap roles.
- Explain the agent-panel concept and reflect on agreement, disagreement and the threshold probe in your own words.
- Review the proposed decision and threshold rationale so they represent your judgment.
- Upload this folder, including its hidden `.agents` directory, to GitHub, then submit the file links through Brightspace → Quizzes → Lab 19. Check Brightspace for the enforced closing time.

## Sources and scope

- [Current Lab 19](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md) and [slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/slides-session-19.md). The raw lab retrieved November 5 agrees on Cathie Wood; an earlier rendered copy mentioning Graham is stale.
- [Lab 18 rules](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md).
- FAskills [Wood](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md), [Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md), and [Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md) as philosophy references only; no plugin installation or paid data.
- [SEC EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces). Snapshots, source tags, annual periods, filing accessions and hashes are saved for reproduction.

Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.
