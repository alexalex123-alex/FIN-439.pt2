"""Run the preserved Lab 18 checks plus Lab 19 calculation and app checks."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', str(ROOT / 'tests'), '-q']))
