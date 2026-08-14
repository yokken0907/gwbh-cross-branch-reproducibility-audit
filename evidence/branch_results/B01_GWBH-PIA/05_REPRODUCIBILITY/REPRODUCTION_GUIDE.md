# Reproduction Guide

## Fast verification
1. Verify the SHA-256 of the master ZIP.
2. Verify `MANIFEST.csv`.
3. Open `02_DATA_AND_PROVENANCE/AUTHORITATIVE_RUN_REGISTER.csv`.
4. Verify any nested RUN ZIP against its adjacent `.sha256`.
5. Use that RUN's README, configuration, code, tests, logs, and outputs.

## Full numerical reproduction
Raw posterior HDF5 files are not duplicated. Each RUN records the public content URL, expected filename, byte size, and checksum.

Use a normal Python virtual environment. Do not override the system package manager.

## Confirmatory integrity
Do not add descriptive post-confirmatory events to new combined p-values. RUN13 and RUN21 remain the authoritative confirmatory results.
