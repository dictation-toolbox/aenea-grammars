# This is a command module for Dragonfly. It provides bindings for the Linux
# window manager Awesome. Only active when running via proxy and the server
# reports Linux.

# You may find this useful to disable the Windows key in windows stealing focus
# from the client.
# http://support.microsoft.com/kb/216893#LetMeFixItMyselfAlways

import aenea
import aenea.misc
import aenea.configuration

import dragonfly

awesome_context = aenea.ProxyPlatformContext('linux')

grammar = dragonfly.Grammar('awesome', context=awesome_context)

awesome = 'W'

from aenea.lax import Key

basics_mapping = aenea.configuration.make_grammar_commands('awesome', {
    'termie': Key(awesome + '-enter'),
    '(whim | notion | ion) screen': Key(awesome + 'c-k'),
    '(whim | notion | ion) up': Key(awesome + '-k'),
    '(whim | notion | ion) down': Key(awesome + '-j'),
    '(whim | notion | ion) left': Key(awesome + 's-k'),
    '(whim | notion | ion) right': Key(awesome + 's-j'),
    '(whim | notion | ion) change screen [<n>]': Key(awesome + '-o:%(n)d'),
    '(whim | notion | ion) close client': Key(awesome + 's-c'),
    '(whim | notion | ion) snap': Key(awesome + 'c-enter'),
    '(whim | notion | ion) full': Key(awesome + '-m'),
    '(whim | notion | ion) [work] <n>': Key(awesome + '-%(n)d'),
    '(whim | notion | ion) tag <n>': Key(awesome + 'sc-%(n)d'),
    '(whim | notion | ion) tag marked <n>': Key(awesome + 's-%(n)d'),
    '(whim | notion | ion) move marked <n>': Key(awesome + 's-%(n)d')
    })


class Basics(dragonfly.MappingRule):
    mapping = basics_mapping
    extras = [aenea.misc.DigitalInteger('n', 1, None)]

grammar.add_rule(Basics())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
