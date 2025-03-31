""" Abstract base class for wrappers. """

from abc import ABC, abstractmethod
import logging
import os

FOLDING_DICTS_PATH = os.path.join(os.path.dirname(__file__), '../folding')

class Wrapper(ABC):

    SUPPORTED_LANGUAGES = []
    WRAPPER_KWARGS_TYPES = {}
    WRAPPER_KWARGS_DEFAULTS = {}
    KWARGS_HELP = {}
    
    @staticmethod
    @abstractmethod
    def supported_languages_message():
        """ Returns a string with the supported languages for the wrapper. """
        pass

    def __init__(self, language, keep_word_boundaries=True, verbose=False, use_folding=True, **wrapper_kwargs):
        """ 
        Initializes the wrapper with the given language and wrapper_kwargs.
        
        Args:
            language (str): The language to phonemize.
            keep_word_boundaries (bool): Whether to keep word boundaries.
            verbose (bool): Whether to print debug information.
            use_folding (bool): Whether to use folding dictionaries to correct the wrapper's output.
            **wrapper_kwargs: Additional keyword arguments.
        
        Raises:
            ValueError: If the language is not supported by the wrapper or if an argument is not supported.
        """

        self.language = language
        self.keep_word_boundaries = keep_word_boundaries
        self.use_folding = use_folding
        self.verbose = verbose
        self.backend_name = self.__class__.__name__.replace('Wrapper', '').lower()

        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.debug(f'Initializing {self.__class__.__name__} with language "{language}" and wrapper_kwargs "{wrapper_kwargs}"')
        
        if not self.check_language_support(language):
            raise ValueError(f'Language "{language}" not supported by {self.__class__.__name__}. Supported languages: {self.get_supported_languages()}')
        
        # Check if wrapper_kwargs are supported
        for key, value in wrapper_kwargs.items():
            if key not in self.WRAPPER_KWARGS_TYPES:
                raise ValueError(f'{self.__class__.__name__} does not accept the "{key}" argument. Supported arguments: {self.WRAPPER_KWARGS_TYPES}')
            if not isinstance(value, self.WRAPPER_KWARGS_TYPES[key]):
                raise ValueError(f'Argument "{key}" must be of type {self.WRAPPER_KWARGS_TYPES[key].__name__}. Got {type(value).__name__} instead.')
            setattr(self, key, value)
        
        # Set default wrapper_kwargs
        for key, value in self.WRAPPER_KWARGS_DEFAULTS.items():
            if key not in wrapper_kwargs:
                setattr(self, key, value)

        # Get folding dicts
        self.folding_dicts = self._get_folding_dictionaries()


    def process(self, lines):
        """ Processes a list of lines by first converting with G2P then possibly applying a folding dictionary."""

        phonemized_lines = self._phonemize(lines)
        for i, line in enumerate(phonemized_lines):
            if line == '' or line == ' ':
                continue
            phonemized_lines[i] = self._post_process_line(line)
        return phonemized_lines

    def check_language_support(self, language):
        """ Checks if the language is supported by the wrapper. 
        
        Returns:
            bool: True if the language is supported, False otherwise.
        """

        if language in self.SUPPORTED_LANGUAGES:
            return True
        return False

    def get_supported_languages(self):
        """ Returns a list of supported languages by the wrapper. """
        return self.SUPPORTED_LANGUAGES

    @abstractmethod
    def _phonemize(self, lines):
        """ Uses a G2P backend to phonemize text. Returns a list of phonemized lines.
        Lines that could not be phonemized should be returned as empty strings ('').
        
        All wrappers should output IPA phonemes separated by spaces. If keep_word_boundaries is True, they should also output 'WORD_BOUNDARY' at the end of each word:

        Example 1 (keep_word_boundaries=True):
        Input: 'hello there!'
        Output: 'h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY'

        Example 2 (keep_word_boundaries=False):
        Input: 'hello there!'
        Output: 'h ə l oʊ ð ɛ ɹ'
        """
        pass

    def _post_process_line(self, line):
        """ Post-processes a phonemized line by applying folding dictionaries and stripping """
        for dict in self.folding_dicts:
            line = ' ' + line + ' ' # For matching items that are at the beginning or end of the line
            for key, value in dict.items():
                line = line.replace(key, value)
            line = line.strip()
        return line

    def _get_folding_dictionaries(self):
        if not self.use_folding:
            self.logger.debug(f"Skipping folding dictionary post-processing, using uncorrected output from {self.backend_name}.")
            return []
        
        # Load main folding dictionary
        main_dict_path = os.path.join(FOLDING_DICTS_PATH, f'{self.backend_name}/{self.backend_name}.csv')
        if os.path.exists(main_dict_path):
            self.logger.debug(f'Found main folding dictionary for {self.backend_name} at {main_dict_path}.')
        else:
            self.logger.debug(f'No folding dictionary for {self.backend_name} found at {main_dict_path}.')
            return []
        dict_paths = [main_dict_path]

        # Load language specific dict
        lang_dict_path = os.path.join(FOLDING_DICTS_PATH, f'{self.backend_name}/{self.language}.csv')
        if os.path.exists(lang_dict_path):
            dict_paths.append(lang_dict_path)
            self.logger.debug(f'Found language-specific folding dictionary at {lang_dict_path}.')
        elif self.backend_name not in ['pinyin_to_ipa', 'pingyam']:
            self.logger.debug(f'No folding dictionary for {self.language} found at {lang_dict_path}.')

        dicts = []
        for dict_path in dict_paths:
            dict = {}
            with open(dict_path, 'r') as f:
                next(f)
                for line in f:
                    key, value = line.strip().split(',')
                    dict[key] = value
            dicts.append(dict)

        return dicts