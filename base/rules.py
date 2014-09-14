from dragonfly import (
    MappingRule,
    CompoundRule,
)

from aenea import (
    Text,
    Dictation
)

from format import FORMAT

import base.characters

__all__ = [
    'AlphaInsertionRule',
    'DigitInsertionRule',
    'AlphaNumInsertionRule',
    'SymbolInsertionRule',
    'CharacterInsertionRule',
    'IdentifierInsertionRule'
]

letters = base.characters.UPPERCASE.copy()
letters.update(base.characters.LOWERCASE.copy())

digits = base.characters.DIGITS.copy()

alpha_num = {}
alpha_num.update(letters)
alpha_num.update(digits)

symbol_chars = {}
symbol_chars.update(base.characters.SYMBOLS_TEXT)

all_chars = alpha_num.copy()
all_chars.update(base.characters.SYMBOLS_TEXT)


class AlphaInsertionRule(MappingRule):
    mapping = dict([(name, Text(letters[name])) for name in letters])


class DigitInsertionRule(MappingRule):
    mapping = dict([("dig " + name, Text(digits[name])) for name in digits])


class AlphaNumInsertionRule(MappingRule):
    mapping = dict([(name, Text(alpha_num[name])) for name in alpha_num])


class SymbolInsertionRule(MappingRule):
    mapping = dict([(name, Text(symbol_chars[name])) for name in symbol_chars])


class CharacterInsertionRule(MappingRule):
    mapping = dict([(name, Text(all_chars[name])) for name in all_chars])


class IdentifierInsertionRule(CompoundRule):
    """
    Rule which formats a dictation using various formatting functions from
    base.format.FORMAT and base.format.CASE.  Rule expects a dictation in the
    following format

    [ caseFunction ] ( formatFunction ) <dictation>

    Where:
        caseFunction is a key name from base.format.CASE
        formatFunction is a key name from base.format.FORMAT
        <dictation> is the dictation to apply the case and format functions to.

    If no case function is given then assume base.format.lower()
    """
    spec = ('[%s] (%s) [<dictation>]' % (
        ' | '.join(base.format.CASE.keys()),
        ' | '.join(base.format.FORMAT.keys())
    ))
    extras = [Dictation(name='dictation')]

    def value(self, node):
        words = node.words()

        if words[0] in base.format.CASE:
            case = words.pop(0)
            format_key = words.pop(0)
            words = base.format.CASE[case](words)
        else:
            format_key = words.pop(0)
            words = base.format.lower(words)

        words = [word.split('\\', 1)[0].replace('-', '') for word in words]

        formatted = FORMAT[format_key](words)

        return Text(formatted)
