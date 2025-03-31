"""
This module provides wrapper classes for various G2P backends.
"""

from .epitran_wrapper import EpitranWrapper
from .phonemizer_wrapper import PhonemizerWrapper
from .pingyam_wrapper import PingyamWrapper
from .pinyin_to_ipa_wrapper import Pinyin_To_IpaWrapper

WRAPPER_BACKENDS = {
    'epitran': EpitranWrapper,
    'phonemizer': PhonemizerWrapper,
    'pingyam': PingyamWrapper,
    'pinyin_to_ipa': Pinyin_To_IpaWrapper,
}