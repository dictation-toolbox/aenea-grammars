import aenea
import config
import personal

if config.PLATFORM == 'proxy':
    from proxy_nicknames import (
        Grammar,
        MappingRule,
        Text
        )
    grammar_context = aenea.global_context
    grammar = Grammar('favorites', context=grammar_context)
else:
    from dragonfly import (
        Grammar,
        MappingRule,
        Text
        )
    grammar = Grammar('favorites')


class Favorites(MappingRule):
    mapping = dict(('fave ' + key, Text(value))
                   for (key, value) in personal.FAVORITES.iteritems())

grammar.add_rule(Favorites())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
