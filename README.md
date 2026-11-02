# Lab 17 — start here

## Files to keep together

| File | Purpose |
|---|---|
| `asof_app.py` | Streamlit page with charts, controls and comparison table. |
| `asof_data.py` | Cached FRED/ALFRED download and comparison functions; required by the app. |
| `lab17.md` | Main submission: data card, reference results, self-review and proposed call. |
| `audit_results.json` | Actual computed audit results, source URLs and retrieval timestamps. |
| `validation.txt` | Checks actually completed by the assistant. |
| `requirements.txt` | Tested Streamlit version. |
| `README.md` | These run and submission instructions. |

## Run on this computer

Open PowerShell and paste:

```powershell
& 'C:\Users\alxsc\Documents\Codex\2026-11-01\can-o\work\lab15\venv\Scripts\python.exe' -m streamlit run 'C:\Users\alxsc\Documents\Codex\2026-11-01\can-o\outputs\lab17\asof_app.py'
```

The existing Lab 15 environment already contains the required dependencies. Internet access is
needed. No FRED account or API key is required. Open the Local URL printed in the terminal if the
browser does not open automatically. Press Ctrl+C to stop.

## Run elsewhere

Open a terminal in this folder with Python installed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run asof_app.py
```

## Walkthrough

1. The app opens with four rates, a January 1, 2020 start and today's as-known date.
2. Set **As known on** to October 5, 2026. Expect BAA 6.47; FEDFUNDS 3.75;
   DGS10 5.28; MORTGAGE30US 7.28. Read their observation dates in the table too.
3. Type **PAYEMS** in the additional-series box and set the cutoff to January 15, 2025.
   Expect December 2024 at 159,536 and many revisions on shared dates.
4. Replace PAYEMS with **CPIAUCSL**. Set the cutoff to October 31, 2026, then November 1, 2026.
   Both show September 2026 at 336.298 in the saved audit. Live data can change later.
5. Try October 5, 2026 for CPI's publication lag and January 15, 2025 for revisions.
6. Read `lab17.md`. Personally confirm its three CPI page values, review the proposed quarantine
   call, and complete its personal checklist.

Chart histories are today's values; the table is where current and historical vintages are compared.
The app does not promise that observation dates are publication dates. Cached downloads expire after
an hour; use **Refresh downloads** for an immediate fresh request. Source failures display errors
and are never replaced with today's data disguised as a historical vintage.

## Submit

Upload the seven files above to a separate `lab17` folder in your GitHub repository. Both Python
files are essential. Submit direct GitHub links through the Lab 17 checkout in Brightspace.
Do not upload `.venv` or `__pycache__`; do not substitute the ZIP for required GitHub file links.
Nothing has been uploaded or submitted by the assistant.
