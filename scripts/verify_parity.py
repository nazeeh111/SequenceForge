"""Compare installed SequenceForge against the retained computational baseline."""

import argparse
import contextlib
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types

BASELINE = "c45591e4c897402ba2ffd3bfcd7cd8b4031d0c09"
ROOT = Path(__file__).resolve().parents[1]


def snapshot(module_name):
    import numpy as np

    module = importlib.import_module(module_name)

    def encode(value):
        if isinstance(value, np.ndarray):
            return {
                "dtype": str(value.dtype),
                "shape": value.shape,
                "values": value.tolist(),
            }
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, (list, tuple)):
            return [encode(item) for item in value]
        if isinstance(value, dict):
            return {str(key): encode(item) for key, item in value.items()}
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    result = []
    for name, algorithm in vars(module).items():
        if (
            name.startswith("_")
            or isinstance(algorithm, (type, types.ModuleType))
            or not hasattr(algorithm, "distance")
        ):
            continue
        for left, right in [
            ("ACTG", "AATG"),
            ("GATTACA", "GCATGCU"),
            ("ABC", "ABC"),
            ("", ""),
            ("A", ""),
        ]:
            for method in (
                "distance",
                "similarity",
                "normalized_distance",
                "normalized_similarity",
                "align",
                "matrix",
            ):
                if not hasattr(algorithm, method):
                    continue
                stream = io.StringIO()
                try:
                    with contextlib.redirect_stdout(stream):
                        value = encode(getattr(algorithm, method)(left, right))
                    outcome = {"value": value}
                except Exception as error:
                    outcome = {"error": type(error).__name__, "message": str(error)}
                result.append(
                    {
                        "algorithm": name,
                        "method": method,
                        "inputs": [left, right],
                        **outcome,
                        "stdout": stream.getvalue(),
                    }
                )
    return result


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("goombay", "sequenceforge"):
        print(json.dumps(snapshot(sys.argv[1]), sort_keys=True, allow_nan=True))
        raise SystemExit(0)
    work = ROOT / ".verification"
    work.mkdir(exist_ok=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        required=True,
        help="Local prior-version checkout containing the goombay package",
    )
    args = parser.parse_args()
    baseline = args.baseline_dir.resolve()
    count = 0
    for source in sorted((baseline / "goombay").rglob("*.py")):
        current = ROOT / "sequenceforge" / source.relative_to(baseline / "goombay")
        assert current.read_text() == source.read_text().replace(
            "Goombay", "SequenceForge"
        ).replace("goombay", "sequenceforge"), source
        count += 1
    assert count == 11, "Expected the complete baseline package"
    original = subprocess.check_output(
        [sys.executable, __file__, "goombay"],
        env=dict(os.environ, PYTHONPATH=str(baseline)),
        cwd=baseline,
    )
    branded = subprocess.check_output(
        [sys.executable, __file__, "sequenceforge"], cwd=ROOT
    )
    assert original == branded, "Computational outputs differ"
    records = json.loads(branded)
    report = {
        "baseline": BASELINE,
        "implementation_files_identical_except_namespace": count,
        "comparisons": len(records),
        "matching_successful_results": sum("value" in record for record in records),
        "matching_errors": sum("error" in record for record in records),
        "output_sha256": hashlib.sha256(branded).hexdigest(),
    }
    (work / "parity-results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
