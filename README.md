# Lab 15 — start here

Keep all files in this folder together. Lab 14's separate files were preserved.

## Files

| File | Purpose |
|---|---|
| `portfolio.py` | Calculations, price estimates and 5-point allocation search; running it still prints Lab 14 baselines. |
| `app.py` | Streamlit controls and results; imports all financial math from the engine. |
| `prices.csv` | Actual adjusted month-end prices for BIL, IEF, LQD and VT. Do not edit to force an answer. |
| `lab15.md` | Main submission: mandate, sources, flowchart, results, self-review and proposed decision. |
| `requirements.txt` | Tested Streamlit version. |
| `validation.txt` | Checks actually completed by the assistant. |
| `README.md` | This setup and walkthrough guide. |

## Start on this computer

Open PowerShell and paste:

```powershell
& 'C:\Users\alxsc\Documents\Codex\2026-11-01\can-o\work\lab15\venv\Scripts\python.exe' -m streamlit run 'C:\Users\alxsc\Documents\Codex\2026-11-01\can-o\outputs\lab15\app.py'
```

Dependencies are already installed in that local environment. If no browser opens, use the Local URL
printed in the terminal, usually http://localhost:8501. Press Ctrl+C in the terminal to stop.

## Start elsewhere

With Python installed, open a terminal in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Do not upload `.venv` or `__pycache__` to GitHub.

## Five-minute walkthrough

1. The app opens in **Meridian training**, with target 6.5% and reserve 3%. Expect weights 0/20/25/55.
2. Set global equity's return to 7%. Expect 0/10/10/80 and a 25-point change. Restore 8%.
3. Choose **Northbridge funds**. Target starts at 5.5%; expect BIL 70%, VT 30%.
4. Upload the supplied `prices.csv` to exercise the upload control; results should stay the same.
5. Check **Use last 36 months**. Expect BIL 90%, VT 10% and a 20-point change.
6. Uncheck it. Reduce VT's displayed return estimate by exactly 1.00 percentage point from the
   unrounded default (subtract 1 from the field's underlying value). Expect BIL 65%, VT 35% and a
   5-point change. Using 9.55% instead of the exact 9.5467689% produces the same grid allocation.
7. Read `lab15.md`, review the proposed pilot decision, and finish its personal checklist.

For the engine-only Lab 14 output, run `python portfolio.py` using your working interpreter.
For the correlation proof, set both `CORRELATIONS[2][3]` and `[3][2]` in `portfolio.py` to 0.50,
save, and refresh the Meridian app. Expect 0/40/0/60. Restore both to 0.25 afterward.

## Submit

Upload these files to a `lab15` folder in your GitHub repository. Submit the direct file links requested
by Brightspace; the main files are `lab15.md`, `portfolio.py`, `app.py`, and `prices.csv`.
This package has not been uploaded to GitHub or submitted to Brightspace.
