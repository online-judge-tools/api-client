import pathlib
import re
from logging import getLogger
from typing import *

from onlinejudge.type import Language, LanguageId

logger = getLogger(__name__)


def select_ids_of_matched_languages(word: str, lang_ids: List[str], language_dict: Dict[str, str], split: bool = False, remove: bool = False) -> List[str]:
    result = []
    for lang_id in lang_ids:
        desc = language_dict[lang_id].lower()
        if split:
            pred = word.lower() in desc.split()
        else:
            pred = word.lower() in desc
        if remove:
            pred = not pred
        if pred:
            result.append(lang_id)
    return result


def is_cplusplus_description(description: str) -> bool:
    # Here, 'clang' is not used as intended. Think about strings like "C++ (Clang)", "Clang++" (this includes "g++" as a substring), or "C (Clang)".
    return 'c++' in description.lower() or 'g++' in description.lower()


def parse_cplusplus_compiler(description: str) -> str:
    """
    :param description: must be for C++
    """

    assert is_cplusplus_description(description)
    if 'clang' in description.lower():
        return 'clang'
    if 'gcc' in description.lower() or 'g++' in description.lower():
        return 'gcc'
    return 'gcc'  # by default


def parse_cplusplus_version(description: str) -> Optional[str]:
    """
    :param description: must be for C++
    """

    assert is_cplusplus_description(description)
    match = re.search(r'[CG]\+\+\s?(\d\w)\b', description)
    if match:
        return match.group(1)
    return None


def is_python_description(description: str) -> bool:
    return 'python' in description.lower() or 'pypy' in description.lower()


def parse_python_version(description: str) -> Optional[int]:
    """
    :param description: must be for Python
    """

    assert is_python_description(description)
    match = re.match(r'([23])\.(?:\d+(?:\.\d+)?|x)', description)
    if match:
        return int(match.group(1))
    match = re.match(r'(?:Python|PyPy) *\(?([23])', description, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def parse_python_interpreter(description: str) -> str:
    """
    :param description: must be for Python
    """

    assert is_python_description(description)
    if 'pypy' in description.lower():
        return 'pypy'
    else:
        return 'cpython'


def guess_language_ids_of_cplusplus_file(filename: pathlib.Path, code: bytes, language_dict: Dict[str, str], *, cxx_latest: bool, cxx_compiler: str) -> List[str]:
    assert cxx_compiler in ('gcc', 'clang', 'all')

    lang_ids = list(language_dict.keys())

    lang_ids = list(filter(lambda lang_id: is_cplusplus_description(language_dict[lang_id]), lang_ids))
    if not lang_ids:
        return []
    logger.debug('all lang ids for C++: %s', lang_ids)

    # compiler
    found_gcc = False
    found_clang = False
    for lang_id in lang_ids:
        compiler = parse_cplusplus_compiler(language_dict[lang_id])
        if compiler == 'gcc':
            found_gcc = True
        elif compiler == 'clang':
            found_clang = True
    if found_gcc and found_clang:
        logger.info('both GCC and Clang are available for C++ compiler')
        if cxx_compiler == 'gcc':
            logger.info('use: GCC')
            lang_ids = list(filter(lambda lang_id: parse_cplusplus_compiler(language_dict[lang_id]) in ('gcc', None), lang_ids))
        elif cxx_compiler == 'clang':
            logger.info('use: Clang')
            lang_ids = list(filter(lambda lang_id: parse_cplusplus_compiler(language_dict[lang_id]) in ('clang', None), lang_ids))
        else:
            assert cxx_compiler == 'all'
    logger.debug('lang ids after compiler filter: %s', lang_ids)

    # version
    if cxx_latest:
        saved_lang_ids = lang_ids
        lang_ids = []
        for compiler in ('gcc', 'clang'):  # use the latest for each compiler
            ids = list(filter(lambda lang_id: parse_cplusplus_compiler(language_dict[lang_id]) in (compiler, None), saved_lang_ids))
            if not ids:
                continue
            ids.sort(key=lambda lang_id: (parse_cplusplus_version(language_dict[lang_id]) or '', language_dict[lang_id]))
            lang_ids += [ids[-1]]  # since C++11 < C++1y < ... as strings
    logger.debug('lang ids after version filter: %s', lang_ids)

    assert lang_ids
    lang_ids = sorted(set(lang_ids))
    return lang_ids


def guess_language_ids_of_python_file(filename: pathlib.Path, code: bytes, language_dict: Dict[str, str], *, python_version: str, python_interpreter: str) -> List[str]:
    assert python_version in ('2', '3', 'auto', 'all')
    assert python_interpreter in ('cpython', 'pypy', 'all')

    lang_ids = list(language_dict.keys())

    # interpreter
    lang_ids = list(filter(lambda lang_id: is_python_description(language_dict[lang_id]), lang_ids))
    if any(parse_python_interpreter(language_dict[lang_id]) == 'pypy' for lang_id in lang_ids):
        logger.info('PyPy is available for Python interpreter')
    if python_interpreter != 'all':
        lang_ids = list(filter(lambda lang_id: parse_python_interpreter(language_dict[lang_id]) == python_interpreter, lang_ids))

    # version
    three_found = False
    two_found = False
    for lang_id in lang_ids:
        version = parse_python_version(language_dict[lang_id])
        logger.debug('%s (%s) is recognized as Python %s', lang_id, language_dict[lang_id], str(version or 'unknown'))
        if version == 3:
            three_found = True
        if version == 2:
            two_found = True
    if two_found and three_found:
        logger.info('both Python2 and Python3 are available for version of Python')
        if python_version in ('2', '3'):
            versions = [int(python_version)]  # type: List[Optional[int]]
        elif python_version == 'all':
            versions = [2, 3]
        else:
            assert python_version == 'auto'
            lines = code.splitlines()
            if code.startswith(b'#!'):
                s = lines[0]  # use shebang
            else:
                s = b'\n'.join(lines[:10] + lines[-5:])  # use modelines
            versions = []
            for version in (2, 3):
                if re.search(r'python *(version:? *)?%d'.encode() % version, s.lower()):
                    versions += [version]
            if not versions:
                logger.info('no version info in code')
                versions = [3]
        logger.info('use: %s', ', '.join(map(str, versions)))
        lang_ids = list(filter(lambda lang_id: parse_python_version(language_dict[lang_id]) in versions + [None], lang_ids))

    lang_ids = sorted(set(lang_ids))
    return lang_ids


other_languages_table: List[Dict[str, Any]] = [
     { 'names': [ 'awk'                   ], 'exts': [ 'awk'       ] },
     { 'names': [ 'bash'                  ], 'exts': [ 'sh'        ] },
     { 'names': [ 'brainfuck'             ], 'exts': [ 'bf'        ] },
     { 'names': [ 'c#'                    ], 'exts': [ 'cs'        ] },
     { 'names': [ 'c'                     ], 'exts': [ 'c'         ], 'split': True },
     { 'names': [ 'ceylon'                ], 'exts': [ 'ceylon'    ] },
     { 'names': [ 'clojure'               ], 'exts': [ 'clj'       ] },
     { 'names': [ 'common lisp'           ], 'exts': [ 'lisp', 'lsp', 'cl' ] },
     { 'names': [ 'crystal'               ], 'exts': [ 'cr'        ] },
     { 'names': [ 'd'                     ], 'exts': [ 'd'         ], 'split': True },
     { 'names': [ 'f#'                    ], 'exts': [ 'fs'        ] },
     { 'names': [ 'fortran'               ], 'exts': [ 'for', 'f', 'f90', 'f95', 'f03' ] },
     { 'names': [ 'go'                    ], 'exts': [ 'go'        ], 'split': True },
     { 'names': [ 'haskell'               ], 'exts': [ 'hs'        ] },
     { 'names': [ 'java'                  ], 'exts': [ 'java'      ] },
     { 'names': [ 'javascript'            ], 'exts': [ 'js'        ] },
     { 'names': [ 'julia'                 ], 'exts': [ 'jl'        ] },
     { 'names': [ 'kotlin'                ], 'exts': [ 'kt', 'kts' ] },
     { 'names': [ 'lua'                   ], 'exts': [ 'lua'       ] },
     { 'names': [ 'nim'                   ], 'exts': [ 'nim'       ] },
     { 'names': [ 'moonscript'            ], 'exts': [ 'moon'      ] },
     { 'names': [ 'objective-c'           ], 'exts': [ 'm'         ] },
     { 'names': [ 'ocaml'                 ], 'exts': [ 'ml'        ] },
     { 'names': [ 'octave'                ], 'exts': [ 'm'         ] },
     { 'names': [ 'pascal'                ], 'exts': [ 'pas'       ] },
     { 'names': [ 'perl6'                 ], 'exts': [ 'p6', 'pl6', 'pm6' ] },
     { 'names': [ 'perl'                  ], 'exts': [ 'pl', 'pm'  ], 'split': True },
     { 'names': [ 'php'                   ], 'exts': [ 'php'       ] },
     { 'names': [ 'ruby'                  ], 'exts': [ 'rb'        ] },
     { 'names': [ 'rust'                  ], 'exts': [ 'rs'        ] },
     { 'names': [ 'scala'                 ], 'exts': [ 'scala'     ] },
     { 'names': [ 'scheme'                ], 'exts': [ 'scm'       ] },
     { 'names': [ 'sed'                   ], 'exts': [ 'sed'       ] },
     { 'names': [ 'standard ml'           ], 'exts': [ 'sml'       ] },
     { 'names': [ 'swift'                 ], 'exts': [ 'swift'     ] },
     { 'names': [ 'text'                  ], 'exts': [ 'txt'       ] },
     { 'names': [ 'typescript'            ], 'exts': [ 'ts'        ] },
     { 'names': [ 'unlambda'              ], 'exts': [ 'unl'       ] },
     { 'names': [ 'vim script'            ], 'exts': [ 'vim'       ] },
     { 'names': [ 'visual basic'          ], 'exts': [ 'vb'        ] },
]  # yapf: disable


def guess_language_ids_of_file(filename: pathlib.Path, code: bytes, language_dict: Dict[str, str], *, cxx_latest: bool, cxx_compiler: str, python_version: str, python_interpreter: str) -> List[str]:
    ext = filename.suffix

    logger.debug('file extension: %s', ext)
    ext = ext.lstrip('.')

    if ext in ('cpp', 'cxx', 'cc', 'C'):
        # memo: https://stackoverflow.com/questions/1545080/c-code-file-extension-cc-vs-cpp
        logger.debug('language guessing: C++')
        return guess_language_ids_of_cplusplus_file(filename, code, language_dict=language_dict, cxx_latest=cxx_latest, cxx_compiler=cxx_compiler)

    elif ext == 'py':
        logger.debug('language guessing: Python')
        return guess_language_ids_of_python_file(filename, code, language_dict=language_dict, python_version=python_version, python_interpreter=python_interpreter)

    else:
        logger.debug('language guessing: others')
        lang_ids = []
        for data in other_languages_table:
            if ext in data['exts']:
                for name in data['names']:
                    lang_ids += select_ids_of_matched_languages(name, list(language_dict.keys()), language_dict=language_dict, split=data.get('split', False))
        return sorted(set(lang_ids))


def guess_languages_of_file(filename: pathlib.Path, code: bytes, languages: List[Language], *, cxx_latest: bool = False, cxx_compiler: str = 'all', python_version: str = 'all', python_interpreter: str = 'all') -> List[Language]:
    language_dict = {str(language.id): language.name for language in languages}
    language_ids = guess_language_ids_of_file(filename, code, language_dict=language_dict, cxx_latest=cxx_latest, cxx_compiler=cxx_compiler, python_version=python_version, python_interpreter=python_interpreter)
    return [Language(LanguageId(language_id), language_dict[language_id]) for language_id in language_ids]
