# Dragonfly module for controlling vim on Linux modelessly. Intended as
# eventual replacement for the vim module.
#

LEADER = 'comma'

try:
    import pkg_resources

    pkg_resources.require('dragonfly >= 0.6.5beta1.dev-r99')
except ImportError:
    pass

import aenea.config

from aenea.raul import (
    DigitalInteger,
    LETTERS,
    DIGITS,
    Nested
    )

if aenea.config.PLATFORM == 'proxy':
    from aenea.proxy_nicknames import (
        Alternative,
        AppContext,
        CompoundRule,
        Dictation,
        MappingRule,
        Grammar,
        Key,
        NoAction,
        Repetition,
        RuleRef,
        Text
        )
    vim_context = AppContext(match='regex', title='(?i).*VIM.*')
    command_t_context = (AppContext(match='regex', title='^GoToFile.*$') &
                         vim_context)
    fugitive_index_context = (AppContext(match='regex', title='^index.*\.git.*$') &
                              vim_context)
    grammar = Grammar('verbal_emacs', context=vim_context)
else:
    from dragonfly import (
        Alternative,
        AppContext,
        CompoundRule,
        MappingRule,
        Grammar,
        Key,
        ActionBase,
        Repetition,
        RuleRef,
        Text
        )

    class NoAction(ActionBase):
        def execute(self):
            pass
    vim_context = AppContext(title='VIM')
    command_t_context = AppContext(title='GoToFile') & vim_context
    fugitive_index_context = (AppContext(title='index') & AppContext('.git') &
                              vim_context)
    grammar = Grammar('verbal_emacs', context=vim_context)


class NumericDelegateRule(CompoundRule):
    def value(self, node):
        delegates = node.children[0].children[0].children
        value = delegates[-1].value()
        if delegates[0].value() is not None:
            value = Text('%s' % delegates[0].value()) + value
        return value


class _DigitalIntegerFetcher(object):
    def __init__(self):
        self.cached = {}

    def __getitem__(self, length):
        if length not in self.cached:
            self.cached[length] = DigitalInteger('count', 1, length)
        return self.cached[length]
ruleDigitalInteger = _DigitalIntegerFetcher()


class LetterMapping(MappingRule):
    mapping = LETTERS
ruleLetterMapping = RuleRef(LetterMapping(), name='LetterMapping')


def execute_insertion_buffer(insertion_buffer):
    if not insertion_buffer:
        return

    if insertion_buffer[0][0] is not None:
        insertion_buffer[0][0].execute()
    else:
        Key('a').execute()

    for insertion in insertion_buffer:
        insertion[1].execute()

    Key('escape:2').execute()

# ****************************************************************************
# IDENTIFIERS
# ****************************************************************************


class InsertModeEntry(MappingRule):
    mapping = {
        'inns': Key('i'),
        'syn': Key('a'),
        'phyllo': Key('o'),
        'phyhigh': Key('O'),
        }
ruleInsertModeEntry = RuleRef(InsertModeEntry(), name='InsertModeEntry')


def format_snakeword(text):
    formatted = text[0][0].upper()
    formatted += text[0][1:]
    formatted += ('_' if len(text) > 1 else '')
    formatted += format_score(text[1:])
    return formatted


def format_score(text):
    return '_'.join(text)


def format_camel(text):
    return text[0] + ''.join([word[0].upper() + word[1:] for word in text[1:]])


def format_proper(text):
    return ''.join(word.capitalize() for word in text)


def format_relpath(text):
    return '/'.join(text)


def format_abspath(text):
    return '/' + format_relpath(text)


def format_scoperesolve(text):
    return '::'.join(text)


def format_jumble(text):
    return ''.join(text)


def format_dotword(text):
    return '.'.join(text)


def format_dashword(text):
    return '-'.join(text)


def format_natword(text):
    return ' '.join(text)


def format_broodingnarrative(text):
    return ''


def format_sentence(text):
    return ' '.join([text[0].capitalize()] + text[1:])


class IdentifierInsertion(CompoundRule):
    spec = ('[upper | natural] ( proper | camel | rel-path | abs-path | score | sentence |'
            'scope-resolve | jumble | dotword | dashword | natword | snakeword | brooding-narrative) [<dictation>]')
    extras = [Dictation(name='dictation')]

    def value(self, node):
        words = node.words()

        uppercase = words[0] == 'upper'
        lowercase = words[0] != 'natural'

        if lowercase:
            words = [word.lower() for word in words]
        if uppercase:
            words = [word.upper() for word in words]

        words = [word.split('\\', 1)[0].replace('-', '') for word in words]
        if words[0].lower() in ('upper', 'natural'):
            del words[0]

        function = globals()['format_%s' % words[0].lower()]
        formatted = function(words[1:])

        return Text(formatted)
ruleIdentifierInsertion = RuleRef(
    IdentifierInsertion(),
    name='IdentifierInsertion'
    )


class LiteralIdentifierInsertion(CompoundRule):
    spec = '[<InsertModeEntry>] literal <IdentifierInsertion>'
    extras = [ruleIdentifierInsertion, ruleInsertModeEntry]

    def value(self, node):
        children = node.children[0].children[0].children
        return [('i', (children[0].value(), children[2].value()))]
ruleLiteralIdentifierInsertion = RuleRef(
    LiteralIdentifierInsertion(),
    name='LiteralIdentifierInsertion'
    )


# ****************************************************************************
# INSERTIONS
# ****************************************************************************

class KeyInsertion(MappingRule):
    mapping = {
        'ace [<count>]':        Key('space:%(count)d'),
        'tab [<count>]':        Key('tab:%(count)d'),
        'slap [<count>]':       Key('enter:%(count)d'),
        'chuck [<count>]':      Key('del:%(count)d'),
        'scratch [<count>]':    Key('backspace:%(count)d'),
        'ack':                  Key('escape'),
        }
    extras = [ruleDigitalInteger[3]]
    defaults = {'count': 1}
ruleKeyInsertion = RuleRef(KeyInsertion(), name='KeyInsertion')


class SymbolInsertion(MappingRule):
    mapping = {
        'amp':        Key('ampersand'),
        'star':       Key('asterisk'),
        'at sign':    Key('at'),
        'back ash':   Key('backslash'),
        'backtick':   Key('backtick'),
        'bar':        Key('bar'),
        'hat':        Key('caret'),
        'yeah':       Key('colon'),
        'drip':       Key('comma'),
        'dollar':     Key('dollar'),
        'dot':        Key('dot'),
        'quote':      Key('dquote'),
        'eek':        Key('equal'),
        'bang':       Key('exclamation'),
        'pound':      Key('hash'),
        'hyph':       Key('hyphen'),
        'percent':    Key('percent'),
        'cross':      Key('plus'),
        'quest':      Key('question'),
        'ash':        Key('slash'),
        'smote':      Key('squote'),
        'tilde':      Key('tilde'),
        'rail':       Key('underscore'),
        'semi':       Key('semicolon'),
        }
ruleSymbolInsertion = RuleRef(SymbolInsertion(), name='SymbolInsertion')


class NestedInsertion(MappingRule):
    mapping = {
        'circle':           Nested('()'),
        'square':           Nested('[]'),
        'box':              Nested('{}'),
        'diamond':          Nested('<>'),
        'nest quote':       Nested('\"\"'),
        'nest smote':       Nested('\'\''),
        }
ruleNestedInsertion = RuleRef(NestedInsertion(), name='NestedInsertion')


class SpellingInsertion(MappingRule):
    mapping = dict(('dig ' + key, val) for (key, val) in DIGITS.iteritems())
    mapping.update(LETTERS)

    def value(self, node):
        return Text(MappingRule.value(self, node))
ruleSpellingInsertion = RuleRef(SpellingInsertion(), name='SpellingInsertion')


class CCppInsertion(MappingRule):
    mapping = {
        'if endif guard':     Text('once') + Key('tab'),

        'include local':      Key('A, E, i, n, c, tab'),
        'include system':     Key('A, E, I, n, c'),
        'define main':        Key('m, a, i, n, tab'),
        'for loop':           Key('A, E, f, o, r, tab'),
        'for int loop':       Key('A, E, f, o, r, i, tab'),
        'while loop':         Key('w, h, tab'),
        'do loop':            Key('d, o, tab'),
        'if test':            Key('i, f, tab'),
        'else clause':        Key('e, l, tab'),
        'if else':            Key('i, f, e, tab'),
        'structure':          Key('A, E, s, t, tab'),
        'function':           Key('A, E, f, u, n, tab'),
        'prototype':          Key('A, E, f, u, n, d, tab'),
        }
ruleCCppInsertion = RuleRef(CCppInsertion(), name='CCppInsertion')


class CppInsertion(MappingRule):
    mapping = {
        'class':              Key('A, E, c, l, tab'),
        'namespace':          Key('A, E, n, s, tab'),

        'hash map':           Key('m, a, p, tab'),
        'tree map':           Key('r, b, t, m, tab'),
        'hash set':           Key('s, e, t, tab'),
        'tree set':           Key('r, b, t, s, tab'),
        'vector':             Key('v, c, tab'),
        'deque':              Key('d, q, tab'),
        'string':             Key('s, r, tab'),
        'cons':               Key('p, r, tab'),
        'tuple':              Key('t, p, tab'),

        'weak pointer':       Key('w, p, tab'),
        'shared pointer':     Key('s, p, tab'),
        'unique pointer':     Key('u, p, tab'),

        'stid':               Key('s, d, tab'),
        'end line':           Key('e, l, tab'),
        'c error':            Key('c, e, tab'),
        'c out':              Key('c, o, tab'),
        'c error line':       Key('c, e, e, tab'),
        'c out line':         Key('c, o, e, tab'),

        'unique pointer ref': Key('c, u, p, r, tab'),

        'alpha omega':        Key('a, o, tab'),
        'back insertor':      Key('b, i, n, s, tab'),
        'inserter':           Key('s, i, n, s, tab'),

        'boost':              Key('b, s, tab'),
        'meth':               Key('m, e, t, h, tab'),

        'null pointer':       Text('nullptr'),

        'range for':          Key('f, o, r, r, tab'),
        'for auto':           Key('f, o, r, a, tab'),
        'forcato':            Key('f, o, r, o, tab'),

        'resolve':            Text('::'),
        'left shift':         Text('<< '),
        'right shift':        Text('>> '),
        }
ruleCppInsertion = RuleRef(CppInsertion(), name='CppInsertion')


class PythonInsertion(MappingRule):
    mapping = {
        'private':          Nested('____'),
        'dub dock string':  Nested('""""""'),
        'dock string':      Nested('\'\'\'\'\'\''),
        'values':           Text('values'),
        'get atter':        Text('getattr'),
        'set atter':        Text('setattr'),
        'has atter':        Text('hasattr'),
        'print':            Text('print'),
        'if test':          Text('if '),
        'elif':             Text('elif '),
        'else':             Text('else'),
        'deaf':             Text('def '),
        'log and':          Text('and '),
        'log or':           Text('or '),
        'log not':          Text('not '),
        'not':              Text('not '),
        'for loop':         Text('for '),
        'as name':          Text('as '),
        'in':               Text('in '),
        'is':               Text('is '),
        'while':            Text('while '),
        'class':            Text('class '),
        'with context':     Text('with '),
        'import':           Text('import '),
        'raise':            Text('raise '),
        'return':           Text('return '),
        'none':             Text('None'),
        'try':              Text('try'),
        'except':           Text('except'),
        'lambda':           Text('lambda '),
        'assert':           Text('assert '),
        'delete':           Text('del '),
        }
rulePythonInsertion = RuleRef(PythonInsertion(), name='PythonInsertion')


class ArithmeticInsertion(MappingRule):
    mapping = {
        'assign':           Text('= '),
        'compare eek':      Text('== '),
        'compare not eek':  Text('!= '),
        'compare greater':  Text('> '),
        'compare less':     Text('< '),
        'compare geck':     Text('>= '),
        'compare lack':     Text('<= '),
        'bit ore':          Text('| '),
        'bit and':          Text('& '),
        'bit ex or':        Text('^ '),
        'times':            Text('* '),
        'divided':          Text('/ '),
        'plus':             Text('+ '),
        'minus':            Text('- '),
        'plus equal':       Text('+= '),
        'minus equal':      Text('-= '),
        'times equal':      Text('*= '),
        'divided equal':    Text('/= '),
        'mod equal':        Text('%%= '),
        }
ruleArithmeticInsertion = RuleRef(
    ArithmeticInsertion(),
    name='ArithmeticInsertion'
    )


class PrimitiveInsertion(CompoundRule):
    spec = '<insertion>'
    extras = [Alternative([
        ruleKeyInsertion,
        ruleSymbolInsertion,
        ruleIdentifierInsertion,
        ruleNestedInsertion,
        rulePythonInsertion,
        ruleArithmeticInsertion,
        ruleCppInsertion,
        ruleCCppInsertion,
        ruleSpellingInsertion,
        ], name='insertion')]

    def value(self, node):
        children = node.children[0].children[0].children
        return children[0].value()
rulePrimitiveInsertion = RuleRef(
    PrimitiveInsertion(),
    name='PrimitiveInsertion'
    )


class PrimitiveInsertionRepetition(CompoundRule):
    spec = '<PrimitiveInsertion> [ parrot <count> ]'
    extras = [rulePrimitiveInsertion, ruleDigitalInteger[3]]

    def value(self, node):
        children = node.children[0].children[0].children
        holder = children[1].value()[1] if children[1].value() else 1
        value = children[0].value() * holder
        return value
rulePrimitiveInsertionRepetition = RuleRef(
    PrimitiveInsertionRepetition(),
    name='PrimitiveInsertionRepetition'
    )


class Insertion(CompoundRule):
    spec = '[<InsertModeEntry>] <PrimitiveInsertionRepetition>'
    extras = [rulePrimitiveInsertionRepetition, ruleInsertModeEntry]

    def value(self, node):
        children = node.children[0].children[0].children
        return [('i', (children[0].value(), children[1].value()))]
ruleInsertion = RuleRef(Insertion(), name='Insertion')


# ****************************************************************************
# MOTIONS
# ****************************************************************************


class PrimitiveMotion(MappingRule):
    mapping = {
        'up': Text('k'),
        'down': Text('j'),
        'left': Text('h'),
        'right': Text('l'),

        'lope': Text('b'),
        'yope': Text('w'),
        'elope': Text('ge'),
        'iyope': Text('e'),

        'lopert': Text('B'),
        'yopert': Text('W'),
        'elopert': Text('gE'),
        'eyopert': Text('E'),

        'apla': Text('{'),
        'anla': Text('}'),
        'sapla': Text('('),
        'sanla': Text(')'),

        'care': Text('^'),
        'hard care': Text('0'),
        'doll': Text('$'),

        'screecare': Text('g^'),
        'screedoll': Text('g$'),

        'scree up': Text('gk'),
        'scree down': Text('gj'),

        'wynac': Text('G'),

        'wynac top': Text('H'),
        'wynac toe': Text('L'),

        # CamelCaseMotion plugin
        'calalope': Text(',b'),
        'calayope': Text(',w'),
        'end calayope': Text(',e'),
        'inner calalope': Text('i,b'),
        'inner calayope': Text('i,w'),
        'inner end calayope': Text('i,e'),

        # EasyMotion
        'easy lope': Key('%s:2, b' % LEADER),
        'easy yope': Key('%s:2, w' % LEADER),
        'easy elope': Key('%s:2, g, e' % LEADER),
        'easy iyope': Key('%s:2, e' % LEADER),

        'easy lopert': Key('%s:2, B' % LEADER),
        'easy yopert': Key('%s:2, W' % LEADER),
        'easy elopert': Key('%s:2, g, E' % LEADER),
        'easy eyopert': Key('%s:2, E' % LEADER),
        }

    for (spoken_object, command_object) in (('(lope | yope)', 'w'),
                                            ('(lopert | yopert)', 'W')):
        for (spoken_modifier, command_modifier) in (('inner', 'i'),
                                                    ('outer', 'a')):
            map_action = Text(command_modifier + command_object)
            mapping['%s %s' % (spoken_modifier, spoken_object)] = map_action
rulePrimitiveMotion = RuleRef(PrimitiveMotion(), name='PrimitiveMotion')


class UncountedMotion(MappingRule):
    mapping = {
        'tect': Text('%%'),
        'matu': Text('M'),
        }
ruleUncountedMotion = RuleRef(UncountedMotion(), name='UncountedMotion')


class MotionParameterMotion(MappingRule):
    mapping = {
        'phytic': 'f',
        'fitton': 'F',
        'pre phytic': 't',
        'pre fitton': 'T',
        }
ruleMotionParameterMotion = RuleRef(
    MotionParameterMotion(),
    name='MotionParameterMotion'
    )


class ParameterizedMotion(CompoundRule):
    spec = '<MotionParameterMotion> <LetterMapping>'
    extras = [ruleLetterMapping, ruleMotionParameterMotion]

    def value(self, node):
        children = node.children[0].children[0].children
        return Text(children[0].value() + children[1].value())
ruleParameterizedMotion = RuleRef(
    ParameterizedMotion(),
    name='ParameterizedMotion'
    )


class CountedMotion(NumericDelegateRule):
    spec = '[<count>] <motion>'
    extras = [ruleDigitalInteger[3],
              Alternative([
                  rulePrimitiveMotion,
                  ruleParameterizedMotion], name='motion')]
ruleCountedMotion = RuleRef(CountedMotion(), name='CountedMotion')


class Motion(CompoundRule):
    spec = '<motion>'
    extras = [Alternative(
        [ruleCountedMotion, ruleUncountedMotion],
        name='motion'
        )]

    def value(self, node):
        return node.children[0].children[0].children[0].value()

ruleMotion = RuleRef(Motion(), name='Motion')


# ****************************************************************************
# OPERATORS
# ****************************************************************************

_OPERATORS = {
    'relo': '',
    'dell': 'd',
    'chaos': 'c',
    'nab': 'y',
    'swap case': 'g~',
    'uppercase': 'gU',
    'lowercase': 'gu',
    'external filter': '!',
    'external format': '=',
    'format text': 'gq',
    'rotate thirteen': 'g?',
    'indent left': '<',
    'indent right': '>',
    'define fold': 'zf',
    }


class PrimitiveOperator(MappingRule):
    mapping = dict((key, Text(val)) for (key, val) in _OPERATORS.iteritems())
    # tComment
    mapping['comm nop'] = Text('gc')
rulePrimitiveOperator = RuleRef(PrimitiveOperator(), name='PrimitiveOperator')


class Operator(NumericDelegateRule):
    spec = '[<count>] <PrimitiveOperator>'
    extras = [ruleDigitalInteger[3],
              rulePrimitiveOperator]
ruleOperator = RuleRef(Operator(), name='Operator')


class OperatorApplicationMotion(CompoundRule):
    spec = '[<Operator>] <Motion>'
    extras = [ruleOperator, ruleMotion]

    def value(self, node):
        children = node.children[0].children[0].children
        return_value = children[1].value()
        if children[0].value() is not None:
            return_value = children[0].value() + return_value
        return return_value
ruleOperatorApplicationMotion = RuleRef(
    OperatorApplicationMotion(),
    name='OperatorApplicationMotion'
    )


class OperatorSelfApplication(MappingRule):
    mapping = dict(('%s [<count>] %s' % (key, key), Text('%s%%(count)d%s' % (value, value)))
                   for (key, value) in _OPERATORS.iteritems())
    # tComment
    # string not action intentional dirty hack.
    mapping['comm nop [<count>] comm nop'] = 'tcomment'
    extras = [ruleDigitalInteger[3]]
    defaults = {'count': 1}

    def value(self, node):
        value = MappingRule.value(self, node)
        if value == 'tcomment':
            # ugly hack to get around tComment's not allowing ranges with gcc.
            value = node.children[0].children[0].children[0].children[1].value()
            if value in (1, '1', None):
                return Text('gcc')
            else:
                return Text('gc%dj' % (int(value) - 1))
        else:
            return value

ruleOperatorSelfApplication = RuleRef(
    OperatorSelfApplication(),
    name='OperatorSelfApplication'
    )

ruleOperatorApplication = Alternative([ruleOperatorApplicationMotion,
                                       ruleOperatorSelfApplication],
                                      name='OperatorApplication')


# ****************************************************************************
# COMMANDS
# ****************************************************************************


class PrimitiveCommand(MappingRule):
    mapping = {
        'vim scratch': Key('X'),
        'vim chuck': Key('x'),
        'vim undo': Key('u'),
        'plap': Key('P'),
        'plop': Key('p'),
        'ditto': Text('.'),
        'ripple': 'macro',
        }
rulePrimitiveCommand = RuleRef(PrimitiveCommand(), name='PrimitiveCommand')


class Command(CompoundRule):
    spec = '[<count>] [reg <LetterMapping>] <command>'
    extras = [Alternative([ruleOperatorApplication,
                           rulePrimitiveCommand,
                           ], name='command'),
              ruleDigitalInteger[3],
              ruleLetterMapping]

    def value(self, node):
        delegates = node.children[0].children[0].children
        value = delegates[-1].value()
        prefix = ''
        if delegates[0].value() is not None:
            prefix += str(delegates[0].value())
        if delegates[1].value() is not None:
            # Hack for macros
            reg = delegates[1].value()[1]
            if value == 'macro':
                prefix += '@' + reg
                value = None
            else:
                prefix += "'" + reg
        if prefix:
            if value is not None:
                value = Text(prefix) + value
            else:
                value = Text(prefix)
        # TODO: ugly hack; should fix the grammar or generalize.
        if 'chaos' in zip(*node.results)[0]:
            return [('c', value), ('i', (NoAction(),) * 2)]
        else:
            return [('c', value)]
ruleCommand = RuleRef(Command(), name='Command')


# ****************************************************************************


class VimCommand(CompoundRule):
    spec = ('[<app>] [<literal>]')
    extras = [Repetition(Alternative([ruleCommand, RuleRef(Insertion())]), max=10, name='app'),
              RuleRef(LiteralIdentifierInsertion(), name='literal')]

    def _process_recognition(self, node, extras):
        insertion_buffer = []
        commands = []
        if 'app' in extras:
            for chunk in extras['app']:
                commands.extend(chunk)
        if 'literal' in extras:
            commands.extend(extras['literal'])
        for command in commands:
            mode, command = command
            if mode == 'i':
                insertion_buffer.append(command)
            else:
                execute_insertion_buffer(insertion_buffer)
                insertion_buffer = []
                command.execute()
        execute_insertion_buffer(insertion_buffer)

grammar.add_rule(VimCommand())

grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
