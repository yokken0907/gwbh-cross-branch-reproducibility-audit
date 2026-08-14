# B08 environment record

Canonical environment recorded for the original B08 analysis:

- Python 3.12.3
- NumPy 2.5.2
- SciPy 1.18.0
- pandas 3.0.5
- Bilby 2.8.2

`requirements.txt` records those package versions exactly.

The public `run_reproduction.py` path consolidates the final corrected Phase4 RUN02 and Phase5 pure-Python metric definitions and therefore does not import NumPy, SciPy, pandas, or Bilby. The environment record is retained to document the canonical analysis context; it is not a claim that other Python environments cannot reproduce the deterministic final metric path.
