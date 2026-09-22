"""Backward-compatible import path for SequenceForge."""

import sys as _sys
import sequenceforge as _implementation
from sequenceforge import *

__path__ = _implementation.__path__
for _name, _module in tuple(_sys.modules.items()):
    if _name.startswith("sequenceforge."):
        _sys.modules[__name__ + _name[len("sequenceforge") :]] = _module
