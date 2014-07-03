# This file is a command-module for Dragonfly.
#
# (based on the multiedit module from dragonfly-modules project)
# (heavily modified)
# (the original copyright notice is reproduced below)
#
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

import aenea
import aenea.misc
import aenea.vocabulary
import aenea.configuration
import aenea.format

from aenea import (
    AeneaContext,
    AppContext,
    Alternative,
    CompoundRule,
    Dictation,
    DictList,
    DictListRef,
    Grammar,
    IntegerRef,
    Literal,
    ProxyAppContext,
    MappingRule,
    NeverContext,
    Repetition,
    RuleRef,
    Sequence
    )

from aenea import (
    Key,
    Text
    )

# Multiedit wants to take over dynamic vocabulary management.
MULTIEDIT_TAGS = ['multiedit', 'multiedit.count']
aenea.vocabulary.inhibit_global_dynamic_vocabulary('multiedit', MULTIEDIT_TAGS)

#---------------------------------------------------------------------------
# Set up this module's configuration.


command_table = aenea.configuration.make_grammar_commands('multiedit', {
    #### Cursor manipulation
    'up [<n>]':    Key('up:%(n)d'),
    'down [<n>]':  Key('down:%(n)d'),
    'left [<n>]':  Key('left:%(n)d'),
    'right [<n>]': Key('right:%(n)d'),

    'gope [<n>]':  Key('pgup:%(n)d'),
    'drop [<n>]':  Key('pgdown:%(n)d'),

    'lope [<n>]':  Key('c-left:%(n)d'),
    'yope [<n>]':  Key('c-right:%(n)d'),

    'care':        Key('home'),
    'doll':        Key('end'),

    'file top':    Key('c-home'),
    'file toe':    Key('c-end'),

    #### Various keys
    'ace [<n>]':         Key('space:%(n)d'),
    'act':               Key('escape'),
    'chuck [<n>]':       Key('del:%(n)d'),
    'scratch [<n>]':     Key('backspace:%(n)d'),
    'slap [<n>]':        Key('enter:%(n)d'),
    'tab [<n>]':         Key('tab:%(n)d'),

    #### Lines
    'line down [<n>]': Key('home:2, shift:down, end:2, shift:up, c-x, del, down:%(n)d, home:2, enter, up, c-v'),
    'lineup [<n>]':    Key('home:2, shift:down, end:2, shift:up, c-x, del, up:%(n)d, home:2, enter, up, c-v'),
    'nab [<n>]':       Key('home:2, shift:down, down:%(n)d, up, end:2, shift:up, c-c, end:2'),
    'plop [<n>]':      Key('c-v:%(n)d'),
    'squishy [<n>]':   Key('end:2, del, space'),
    'strip':           Key('s-end:2, del'),
    'striss':          Key('s-home:2, del'),
    'trance [<n>]':    Key('home:2, shift:down, down:%(n)d, up, end:2, shift:up, c-c, end:2, enter, c-v'),
    'wipe [<n>]':      Key('home:2, shift:down, down:%(n)d, up, end:2, del, shift:up, backspace'),

    #### Words
    'bump [<n>]':      Key('cs-right:%(n)d, del'),
    'whack [<n>]':     Key('cs-left:%(n)d, del'),
    }, config_key='commands')


class FormatRule(CompoundRule):
    spec = ('[upper | natural] ( proper | camel | rel-path | abs-path | score | sentence | '
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

        function = getattr(aenea.format, 'format_%s' % words[0].lower())
        formatted = function(words[1:])

        return Text(formatted)


#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these
#  include special elements like the number with name 'n'
#  or the dictation with name 'text'.  This rule is not
#  exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its 'value' when
#  processing a recognition will be the right side of the
#  mapping: an action.
# Note that this rule does not execute these actions, it
#  simply returns them when it's value() method is called.
#  For example 'up 4' will give the value Key('up:4').
# More information about Key() actions can be found here:
#  http://dragonfly.googlecode.com/svn/trunk/dragonfly/documentation/actionkey.html


class KeystrokeRule(MappingRule):
    exported = False

    extras = [
        IntegerRef('n', 1, 100),
        Dictation('text'),
        Dictation('text2'),
        ]

    defaults = {
        'n': 1,
        }


# TODO: this can NOT be the right way to do this...
class NumericDelegateRule(CompoundRule):
    def value(self, node):
        delegates = node.children[0].children[0].children
        value = delegates[0].value()
        if delegates[-1].value() is not None:
            return value * int(delegates[-1].value())
        else:
            return value


class StaticCountRule(NumericDelegateRule):
    spec = '<static> [<n>]'

    extras = [
        IntegerRef('n', 1, 100),
        DictListRef(
            'static',
            DictList(
                'static multiedit.count',
                aenea.vocabulary.get_static_vocabulary('multiedit.count')
                )),
        ]

class DynamicCountRule(NumericDelegateRule):
    spec = '<dynamic> [<n>]'

    extras = [
        IntegerRef('n', 1, 100),
        DictListRef('dynamic', aenea.vocabulary.register_dynamic_vocabulary('multiedit.count')),
        ]

    defaults = {
        'n': 1,
        }

#---------------------------------------------------------------------------
# Here we create an element which is the sequence of keystrokes.

# First we create an element that references the keystroke rule.
#  Note: when processing a recognition, the *value* of this element
#  will be the value of the referenced rule: an action.


mapping = dict((key, val) for (key, val) in command_table.iteritems())

format_rule = RuleRef(name='format_rule', rule=FormatRule(name='i'))
alternatives = [
    RuleRef(rule=KeystrokeRule(mapping=mapping, name='c')),
    DictListRef(
        'dynamic multiedit',
        aenea.vocabulary.register_dynamic_vocabulary('multiedit')
        ),
    DictListRef(
        'static multiedit',
        DictList(
            'static multiedit',
            aenea.vocabulary.get_static_vocabulary('multiedit')
            ),
        ),
    RuleRef(rule=DynamicCountRule(name='aoeuazzzxt'), name='aouxxxazsemi'),
    RuleRef(rule=StaticCountRule(name='aioeuazzzxt'), name='aouxxxazsemii'),
    format_rule,
    ]

single_action = Alternative(alternatives)

# Can only be used as the last element
alphabet_mapping = dict((key, Text(value))
                        for (key, value) in aenea.misc.LETTERS.iteritems())
numbers_mapping = dict((key, Text(value))
                        for (key, value) in aenea.misc.DIGITS.iteritems())
alphanumeric_mapping = dict((key, Text(value))
                            for (key, value) in aenea.misc.ALPHANUMERIC.iteritems())

alphabet_rule = Sequence([Literal('letters'), Repetition(RuleRef(name='x', rule=MappingRule(name='t', mapping=alphabet_mapping)), min=1, max=20)])
numbers_rule = Sequence([Literal('digits'), Repetition(RuleRef(name='y', rule=MappingRule(name='u', mapping=numbers_mapping)), min=1, max=20)])
alphanumeric_rule = Sequence([Literal('alphanumeric'), Repetition(RuleRef(name='z', rule=MappingRule(name='v', mapping=alphanumeric_mapping)), min=1, max=20)])
finishes = [alphabet_rule, numbers_rule, alphanumeric_rule]

# Second we create a repetition of keystroke elements.
#  This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element
#  the name 'sequence' so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element
#  will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name='sequence')

extras = [
    sequence,  # Sequence of actions defined above.
    IntegerRef('n', 1, 100),  # Times to repeat the sequence.
    Alternative([Literal('hi')], name='finish'),
    ]

#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.


class LiteralRule(CompoundRule):
    spec = 'literal <format_rule>'

    extras = [format_rule]

    def _process_recognition(self, node, extras):
        extras['format_rule'].execute(extras)

# This is the rule that actually handles recognitions.
#  When a recognition occurs, it's _process_recognition()
#  method will be called.  It receives information about the
#  recognition in the 'extras' argument: the sequence of
#  actions and the number of times to repeat them.

class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = '[ <sequence> ] [ ( literal <format_rule> )  | <finish> ] [repeat <n> times]'

    
    defaults = {
        'n': 1, # Default repeat count.
        }

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the 'extras' special elements:
    #   . extras['sequence'] gives the sequence of actions.
    #   . extras['n'] gives the repeat count.
    def _process_recognition(self, node, extras):
        sequence = extras.get('sequence', [])
        count = extras['n']
        for i in range(count):
            for action in sequence:
                action.execute(extras)
            if 'format_rule' in extras:
                extras['format_rule'].execute(extras)
            if 'finish' in extras:
                for action in extras['finish'][1]:
                    action.execute(extras)

#---------------------------------------------------------------------------
# Create and load this module's grammar.

conf = aenea.configuration.ConfigWatcher(('grammar_config', 'multiedit')).conf

local_disable_setting = conf.get('local_disable_context', None)
local_disable_context = NeverContext()
if local_disable_setting is not None:
    if not isinstance(local_disable_setting, basestring):
        print 'Local disable context may only be a string.'
    else:
        local_disable_context = AppContext(str(local_disable_setting))



proxy_disable_setting = conf.get('proxy_disable_context', None)
proxy_disable_context = NeverContext()
if proxy_disable_setting is not None:
    if isinstance(proxy_disable_setting, dict):
        d = {}
        for k, v in proxy_disable_setting.iteritems():
            d[str(k)] = str(v)
        proxy_disable_context = ProxyAppContext(**d)
    else:
        proxy_disable_context = ProxyAppContext(
            title=str(proxy_disable_setting),
            match='substring'
            )


context = AeneaContext(proxy_disable_context, local_disable_context)

grammar = Grammar('multiedit', context=~context)
grammar.add_rule(RepeatRule(extras=extras + [format_rule, Alternative(finishes, name='finish')], name='a'))
grammar.add_rule(LiteralRule())

grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    aenea.vocabulary.uninhibit_global_dynamic_vocabulary(
        'multiedit',
        MULTIEDIT_TAGS
        )
    for tag in MULTIEDIT_TAGS:
        aenea.vocabulary.unregister_dynamic_vocabulary(tag)
    if grammar:
        grammar.unload()
    grammar = None
