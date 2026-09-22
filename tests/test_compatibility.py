import goombay
import sequenceforge
from goombay.align.edit import NeedlemanWunsch as LegacyNeedlemanWunsch
from sequenceforge.align.edit import NeedlemanWunsch


def test_legacy_imports_share_the_same_implementation():
    assert goombay.needleman_wunsch is sequenceforge.needleman_wunsch
    assert LegacyNeedlemanWunsch is NeedlemanWunsch
