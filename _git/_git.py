import aenea.config
import aenea.configuration

from aenea.proxy_contexts import ProxyAppContext

from dragonfly import (
    AppContext,
    Grammar,
    RuleRef,
    MappingRule,
    Alternative,
    CompoundRule,
)

from aenea import (
    Key,
    Text,
)

# TODO
import json

#  from aenea import Text

# TODO What is aenea.configuration.make_grammar_commands


class GitCommandRule(CompoundRule):
    def value(self, node):
        try:
            json.dumps(node)
            pass
        except Exception as e:
            print(e)


class GitRule(CompoundRule):
    spec = 'git [command] [<cancel>] [<enter>]'
    extras = [
        #          Alternative(name='command', children=[
        #              RuleRef(name='add', rule=GitCommandRule(
        #                  name='add',
        #              )),
        #          ]),
        RuleRef(name='cancel', rule=MappingRule(name='cancel', mapping={'cancel': Key('c-c')})),
        RuleRef(name='enter', rule=MappingRule(name='enter', mapping={'enter': Key('enter')})),
    ]

    def _process_recognition(self, node, extras):
        print('extras', extras)
        for name, executable in extras.iteritems():
#              executable.execute()
            print(name, executable)


context = aenea.wrappers.AeneaContext(
    ProxyAppContext(
        match='regex',
        app_id='(?i)(?:(?:DOS|CMD).*)|(?:.*(?:TERM|SHELL).*)',
    ),
    AppContext(title='git'),
)
git_grammar = Grammar('git', context=context)
git_grammar.add_rule(GitRule())
git_grammar.load()


def unload():
    global git_grammar
    if git_grammar:
        git_grammar.unload()
    git_grammar = None
