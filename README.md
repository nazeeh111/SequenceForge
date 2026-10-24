# SequenceForge

**Align sequences. Inspect every score.** A Python toolkit for global, local, and multiple sequence alignment, edit distances, overlap measures, and phylogenetic trees.

[Algorithm reference](docs/API.md) · [Examples](examples) · [Verification](docs/VERIFICATION.md)

## Start in minutes

```bash
git clone https://github.com/nazeeh111/SequenceForge.git
cd SequenceForge
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Python 3.10 or later is required. Installation pulls NumPy, Biopython, and Biobase. This repository is the installation source; no separate package-registry release is implied.

```python
from sequenceforge import (
    needleman_wunsch as nw,
)

alignment = nw.align("ACGT", "AGT")
print(alignment)
# ACGT
# A-GT

scores, pointers = nw.matrix("ACGT", "AGT")
assert scores.shape == pointers.shape == (5, 4)
assert nw.similarity("ACGT", "AGT") == 4
```

![Needleman-Wunsch alignment of ACGT and AGT, with its score matrix and returned alignment path](docs/alignment-example.svg)

The default rewards a match by 2 and subtracts 1 for a mismatch or 2 for a gap. This alignment earns `3 × 2 − 2 = 4`. The highlighted cells follow the returned alignment; other inputs can have tied alignments. [Exact example data](docs/alignment-example.json).

## Choose the comparison

| Task | Available approaches |
| --- | --- |
| Global alignment | Needleman–Wunsch, Gotoh, Waterman–Smith–Beyer, Hirschberg |
| Local alignment | Smith–Waterman, local Gotoh, local Waterman–Smith–Beyer |
| Edit and string distance | Hamming, Wagner–Fischer, Lowrance–Wagner, Jaro, Jaro–Winkler |
| Shared structure | Common subsequences, substrings, supersequences, prefixes, postfixes |
| Multiple sequences | Feng–Doolittle and longest-common-substring alignment |
| Phylogenetic trees | Neighbor joining and Newick formatting |

Classes expose configurable parameters; ready-to-use instances provide defaults. Method availability differs by algorithm. Consult the [complete implementation table](docs/API.md#implementation) before choosing alignment, score, or matrix methods. Supported constructors accept `substitution_matrix`, using nested residue lookup such as `matrix["A"]["C"]`. See the reference for the actual keyword names and defaults.

Scores and returned objects differ across methods. Known edge cases affect distance, normalization and some matrix helpers; check the [current limitations](docs/API.md#caveats) before using a score as a metric or probability.

## Verify and develop

**Development history:** Developed locally using Git before publication. These projects were published to GitHub together, so similar upload dates do not indicate when development began.

```bash
python -m pytest -q
```

The primary namespace is `sequenceforge`; existing `goombay` imports remain supported through a compatibility package. Numerical algorithms, scoring defaults, returned alignment strings, and matrices are preserved. [Verification details](docs/VERIFICATION.md) distinguish tested parity from broader guarantees. Scoring and input limitations remain documented in the [algorithm caveats](docs/API.md#caveats).

Maintained by [nazeeh111](https://github.com/nazeeh111).
