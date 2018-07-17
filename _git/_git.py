import aenea.config
import aenea.configuration

from aenea.proxy_contexts import ProxyAppContext

from dragonfly import (
    Alternative,
    AppContext,
    CompoundRule,
    Grammar,
    MappingRule,
    Repetition,
    RuleRef,
)

from aenea import (
    Key,
    Text,
)

# TODO
import json

#  from aenea import Text

# TODO What is aenea.configuration.make_grammar_commands


#  class GitCommandOptionRule(MappingRule):
#      def __init__(self, possible_options):
#          super(GitCommandRule, self).__init__(
#              mapping=possible_options
#          )


class GitCommandRule(CompoundRule):
    def __init__(self, name, options, command_alias=None):
        if command_alias is None:
            command_alias = name

        super(GitCommandRule, self).__init__(
            spec=command_alias + ' <options>',
            extras=[Repetition(
                name='options',
                min=0,
                max=10,
                child=RuleRef(MappingRule(
                    name=name + '_options',
                    mapping=options,
                )),
            )],
        )

    def value(self, node):
        try:
            json.dumps(node)
            pass
        except Exception as e:
            print(e)


class GitRule(CompoundRule):
    spec = 'git [<command>] [<enter>] [<cancel>]'
    extras = [
        Alternative(name='command', children=[
            RuleRef(name='add', rule=GitCommandRule(
                name='add',
                options={
                    'all': Text('--all '),
                    'dot|point': Text('. '),
                }
            )),
        ]),
        RuleRef(name='enter', rule=MappingRule(
            name='enter',
            mapping={'enter': Key('enter')},
        )),
        RuleRef(name='cancel', rule=MappingRule(
            name='cancel',
            mapping={'cancel': Key('c-c')},
        )),
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
