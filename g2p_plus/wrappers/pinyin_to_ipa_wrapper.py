""" 
Wrapper for converting Mandarin pinyin text to IPA phonemes.

This wrapper uses the pinyin_to_ipa library to convert Mandarin Chinese written in 
pinyin (romanized) format to International Phonetic Alphabet (IPA) notation. It 
handles both numbered and unnumbered pinyin formats.
"""

import re

from pinyin_to_ipa import pinyin_to_ipa
from g2p_plus.wrappers.wrapper import Wrapper

class Pinyin_To_IpaWrapper(Wrapper):
    """
    Wrapper for converting Mandarin pinyin to IPA phonemes.

    This wrapper processes text written in pinyin (e.g. "ni3 hao3") and converts it
    to space-separated IPA phonemes. It can handle both numbered tones (ni3) and 
    unnumbered pinyin text.

    Class Attributes:
        SUPPORTED_LANGUAGES (list): Contains only 'mandarin' as this wrapper is
            specifically for Mandarin Chinese
    """

    SUPPORTED_LANGUAGES = ['mandarin']

    @staticmethod
    def supported_languages_message():
        """
        Returns information about language support for this wrapper.

        Returns:
            str: Message indicating this wrapper only supports Mandarin Chinese
        """
        message = 'The PinyinToIpaWrapper uses the pinyin_to_ipa library, which only supports `mandarin`.\n'
        return message
    
    def _phonemize(self, lines):
        """ 
        Converts pinyin text to IPA phonemes.

        The method splits each line into words, then processes each word's syllables
        individually. It handles both numbered pinyin (e.g. "ni3") and unnumbered
        pinyin text.

        Args:
            lines (list[str]): List of pinyin text strings to convert

        Returns:
            list[str]: List of phonemized strings where each phoneme is separated by
                      spaces. Failed conversions return empty strings.

        Examples:
            With keep_word_boundaries=True:
                Input: "ni3 hao3"
                Output: "n i ˨˩˦ WORD_BOUNDARY x aʊ̯ ˨˩˦ WORD_BOUNDARY"

            With keep_word_boundaries=False:
                Input: "ni3 hao3"
                Output: "n i ˨˩˦ x aʊ̯ ˨˩˦"
        """
        phonemized_utterances = []
        broken = 0
        for line in lines:
            if line.strip() == '':
                phonemized_utterances.append('')
                continue

            phonemized = ""
            words = line.split(' ')
            try:
                for word in words:
                    # Extract pinyin syllables, handling both numbered and unnumbered formats
                    syllables = re.findall(r'[a-zA-Z]+[0-9]*', word)
                    # Remove any '0' tone markers as they're not needed
                    syllables = [re.sub(r'[0]', '', syllable) for syllable in syllables]
                    
                    for syllable in syllables:
                        syll_set = pinyin_to_ipa(syllable)
                        syll = ' '.join(syll_set[0])
                        phonemized += syll + ' '
                    
                    if self.keep_word_boundaries:
                        phonemized += 'WORD_BOUNDARY '
            except Exception as e:
                phonemized = ""
                broken += 1

            phonemized_utterances.append(phonemized)

        if broken > 0:
            self.logger.debug(f'WARNING: {broken} lines were not phonemized successfully by pinyin to ipa conversion.')
        
        return phonemized_utterances


