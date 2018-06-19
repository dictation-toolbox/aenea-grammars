import aenea.config
import aenea.configuration

from aenea.proxy_contexts import ProxyAppContext

from dragonfly import (
    AppContext,
    Grammar,
    MappingRule,
    RuleRef,
    Repetition,
    Alternative,
    CompoundRule,
)

from aenea import Text

# TODO What is aenea.configuration.make_grammar_commands


class GitAddRule(CompoundRule):
    spec = "add [<add_options>]"
    extras = [add_options]

    def value(self, node):
        try:
            # TODO
            pass
        except Exception as e:
            print(e)
add_rule = RuleRef(name='add_rule', rule=GitAddRule())


class GitAddOptionRule(MappingRule):
    spec = {
        'hello': 'hello ',
        'world': 'world ',
    }


add_option = RuleRef(name='add_option', rule=GitAddOptionRule())
add_options = Repetition(add_option, min=1, max=10, name='add_options')


# TODO generate children with dsl
git_command = Alternative(name='command', children=[
    add_rule,
])


class TopLevelRule(CompoundRule):
    spec = 'git <command>'
    extras = [git_command]

    def process_recognition(self, node):
        self.value(node).execute()


context = aenea.wrappers.AeneaContext(
    ProxyAppContext(
        match='regex',
        app_id='(?i)(?:(?:DOS|CMD).*)|(?:.*(?:TERM|SHELL).*)',
    ),
    AppContext(title='git'),
)
git_grammar = Grammar('git', context=context)
git_grammar.add_rule(TopLevelRule())
git_grammar.load()


def unload():
    global git_grammar
    if git_grammar:
        git_grammar.unload()
    git_grammar = None
