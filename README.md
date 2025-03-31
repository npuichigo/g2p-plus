# G2P+

This repository contains scripts for converting various corpora to a unified IPA format, with marked word and utterance boundaries, to prepare them for [training and evaluating small transformer-based language models](https://github.com/codebyzeb/PhonemeTransformers).

It leverages four existing G2P tools (two statistical tools and two pronunciation dictionaries) to support a wide variety of languages:

| Backend        | Languages   |
|------------------|--------|
| [phonemizer](https://github.com/bootphon/phonemizer)           | 100+ languages/accents    |
| [epitran](https://github.com/dmort27/epitran)          | 149 languages/scripts     |
| [pinyin-to-ipa](https://github.com/stefantaubert/pinyin-to-ipa)         | 1 (Mandarin)     |
| [pingyam](https://github.com/kfcd/pingyam/blob/master/pingyambiu)           | 1 (Cantonese)     |


## Installation

The simplest way is using pip:

```
pip install g2p-plus
```

Or you can install from source:

```
git clone https://github.com/codebyzeb/g2p-plus
cd g2p-plus
pip install .
```

### Dependencies

The `phonemizer` backend requires [`espeak-ng`](https://github.com/espeak-ng/espeak-ng) to be installed. See instructions [here](https://bootphon.github.io/phonemizer/install.html).

On mac, the backend requires `PHONEMIZER_ESPEAK_LIBRARY` to be set in the local environment. You may find that before running g2p_plus, you need to add this to your environment, e.g.:

```
export PHONEMIZER_ESPEAK_LIBRARY=/opt/local/lib/libespeak-ng.dylib
```

The `epitran` backend with English requires Flite to be installed. See instructions [here](https://github.com/dmort27/epitran#installation-of-flite-for-english-g2p). 

## Usage

G2P+ is available as a command-line tool or as a python function. 

### Command-line interface

`g2p_plus` is the CLI for G2P+, supporting the conversion of corpora to a unified IPA format. It supports multiple backends, as described above. The help menu (`-h`) describes usage and the languages supported by each backend. The script reads lines from an input file (using `-i`) and saves space-separated IPA phonemes to an output file (using `-o`) or reads/writes to/from STDIN/STDOUT if files are not provided. Word boundaries are provided between words using `-k` using a `WORD_BOUNDARY` token.

For many languages, the underlying transcription tool does not output phoneme sets that match typical phoneme inventories for that language. As such, we have implemented "folding" dictionaries for many languages. These map the output of a backend for a language to a standard phoneme inventory in [Phoible](https://phoible.org/). See `g2p_plus/folding` for these dictionaries. This "folding" can be turned off using `-u`. 

Example usage:

```
> g2p_plus phonemizer en-gb -k
hello there!
h ə l əʊ WORD_BOUNDARY ð eə WORD_BOUNDARY

> g2p_plus phonemizer en-us
hello there!
h ə l oʊ ð ɛ ɹ
```

### Python library

G2P+ can be imported in python and used as follows:

```
from g2p_plus import phonemize_utterances
lines = ['hello there!', 'nice to meet you.']
phonemized = phonemize_utterances(lines, "phonemizer", "en-gb", keep_word_boundaries=True)
```

## Attribution

This project incorporates content from the following sources:

<!-- - **Phoible** by **Moran, Steven & McCloy, Daniel**, licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).  
  Original work: [https://phoible.org/](https://phoible.org/)  -->
- **Pingyam** by **Open Dictionary**, licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).  
  Original work: [https://github.com/kfcd/pingyam/tree/master](https://github.com/kfcd/pingyam/tree/master) 
- **CEDICT** by **MDBG**, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).  
  Original work: [https://www.mdbg.net/chinese/dictionary?page=cc-cedict](https://www.mdbg.net/chinese/dictionary?page=cc-cedict) 

In accordance with the **CC BY-SA 3.0** license, any derivative work or adaptation of these resources must also be shared under the same license.

## License

All original content in this repository created by **Zébulon Goriely** is licensed under the [MIT License](https://github.com/codebyzeb/g2p-plus/blob/main/LICENSE). 