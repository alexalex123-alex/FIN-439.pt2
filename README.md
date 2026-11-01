# Lab 16 — start here

## Files

| File | Purpose |
|---|---|
| `asof.py` | Standard-library Python filter; editable data and cutoff at the top. |
| `lab16.md` | Main write-up: concepts, results, worked yields, self-review and reflection. |
| `output.txt` | Actual output for March 31 and April 15. |
| `validation.txt` | Checks actually run by the assistant. |
| `README.md` | This setup and submission guide. |

## Run on this computer

Open PowerShell and paste:

```powershell
Set-Location -LiteralPath 'C:\Users\alxsc\Documents\Codex\2026-11-01\can-o\outputs\lab16'
& 'C:\Users\alxsc\AppData\Local\Python\pythoncore-3.14-64\python.exe' asof.py
& 'C:\Users\alxsc\AppData\Local\Python\pythoncore-3.14-64\python.exe' asof.py --decision-date 2026-04-15
```

On another computer with a working Python command, use `python asof.py` and
`python asof.py --decision-date 2026-04-15`. No packages, installation step or API key are needed.
The command-line probe leaves the default cutoff unchanged.

## Walkthrough

1. Open `asof.py`: find `TABLE` and `DECISION_DATE` at the top.
2. Follow `clean_records`, `asof_panel`, and `latest_vintages` in that order.
3. Run the program. Compare the funnel and six retained row IDs against `output.txt`.
4. Read `signals`: it compares adjacent observation months, not publication dates.
5. Run the April 15 command. All three as-of signals should match the naive signals.
6. Read the separate sanity review: chronology and financial plausibility are different checks.
7. Review `lab16.md`: your comprehension answer is recorded. Complete the remaining personal checklist.

## Submit

Upload these five files to a separate `lab16` folder in your GitHub repository. The core submissions
are `asof.py` and `lab16.md`; the other files supply run evidence and instructions. Submit the direct
GitHub file links through the Lab 16 checkout in Brightspace. Do not upload `__pycache__`.

The ZIP is a convenient download, not a substitute for the requested GitHub file links.
No GitHub upload or Brightspace submission has been performed. Lab 17 is outside this package.
