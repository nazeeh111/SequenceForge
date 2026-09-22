# Verification

Verified locally on 2026-09-22 using Python 3.12.13 on macOS ARM64.

- Baseline test suite: 257 tests and 430 subtests passed.
- Branded package: 258 tests and 430 subtests passed, including legacy-import object identity.
- 710 direct baseline comparisons matched: 646 successful results and 64 matching errors across alignment, scoring, normalized metrics, matrices, and five representative input pairs. Empty-input errors are preserved, not represented as successful calculations.
- All 11 computational implementation files match the baseline exactly after replacing the package namespace. Algorithms, scoring defaults, and matrix operations were not refactored.
- Wheel build succeeded. Installation into a fresh isolated environment passed both `sequenceforge` and legacy `goombay` import checks and a real alignment smoke test.
- Black 25.12 formatting and Flake8 fatal-error checks passed.

The [parity record](parity-results.json) contains counts and a hash of the compared output. The exact development environment is recorded in `requirements-dev-lock.txt`; those full environment pins target Python 3.12 rather than every Python version supported by the library.

## Repeat checks

```bash
python -m pytest -q
python -m black --check sequenceforge goombay tests scripts
python -m flake8 sequenceforge goombay tests scripts --select=E9,F63,F7,F82
```

For parity against a separately retained prior checkout:

```bash
python scripts/verify_parity.py --baseline-dir /path/to/previous-checkout
```

The baseline directory must contain its original `goombay` package. No historical Git objects are required in this repository; an explicit local baseline is required for that comparison. Ordinary tests and installation work in a clean clone.

## Limits

These tests establish the reported cases, not universal correctness for every sequence and scoring matrix. Existing unsupported operations, empty-input behavior, and algorithm caveats remain. Notebook examples were preserved and their imports updated, but external-data notebook workflows were not rerun. Only the reported Python/macOS environment was executed locally; CI defines additional platforms/versions without claiming they already passed.
