# SequenceForge

Compare sequences with ready-to-use alignment algorithms, then inspect the alignment, score or distance, and calculation matrix through a common Python interface. SequenceForge also includes overlap measures and phylogenetic trees. Methods vary by algorithm; the [reference table](docs/API.md#implementation) shows what each one supports.

[Algorithm reference](docs/API.md) · [Examples](examples) · [Verification](docs/VERIFICATION.md)

## Installation

```bash
git clone https://github.com/nazeeh111/SequenceForge.git
cd SequenceForge
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
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

scores = nw.matrix("ACGT", "AGT")
assert len(scores) == 5
assert len(scores[0]) == 4
```

## Choose the comparison

| Task | Available approaches |
| --- | --- |
| Global alignment | Needleman–Wunsch, Gotoh, Waterman–Smith–Beyer, Hirschberg |
| Local alignment | Smith–Waterman, local Gotoh, local Waterman–Smith–Beyer |
| Edit and string distance | Hamming, Wagner–Fischer, Lowrance–Wagner, Jaro, Jaro–Winkler |
| Shared structure | Common subsequences, substrings, supersequences, prefixes, postfixes |
| Multiple sequences | Feng–Doolittle and longest-common-substring alignment |
| Phylogenetic trees | Neighbor joining and Newick formatting |

Classes expose configurable parameters; ready-to-use instances provide defaults. Method availability differs by algorithm. Consult the [complete implementation table](docs/API.md#implementation) before choosing alignment, score, or matrix methods. The `scoring_matrix` parameter accepts supported Biobase substitution matrices.

## Verify and develop

```bash
python -m pytest -q
```

Install developer tools with `python -m pip install -e ".[dev]"` before running pytest. The primary namespace is `sequenceforge`; existing `goombay` imports remain supported through a compatibility package. Numerical algorithms, scoring defaults, returned alignment strings, and matrices are preserved. [Verification details](docs/VERIFICATION.md) distinguish tested parity from broader guarantees. Scoring and input limitations remain documented in the [algorithm caveats](docs/API.md#caveats).

Maintained by [nazeeh111](https://github.com/nazeeh111).
