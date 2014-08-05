import aenea.config
import aenea.configuration

from aenea import (
    AeneaContext,
    AppContext,
    Dictation,
    Grammar,
    IntegerRef,
    Key,
    MappingRule,
    ProxyAppContext,
    Text,
    MappingRule,
    RuleRef,
    Repetition,
    Alternative,
    CompoundRule,
    )


class GitAddOptionRule(MappingRule):
    mapping = {
        'all': '--all ',
        'force': '--force ',
        'ignore errors': '--ignore-errors ',
        'no all': '--no-all ',
        'ignore removal': '--ignore-removal ',
    }
add_option_rule = RuleRef(name='add_option', rule=GitAddOptionRule())
add_option_rules = Repetition(add_option_rule, min=1, max=10, name='add_options')


class GitAddRule(CompoundRule):
    spec = "add [<add_options>]"
    extras = [add_option_rules]
git_add_rule = RuleRef(name='add_rule', rule=GitAddRule())


class GitCommitOptionRule(MappingRule):
    mapping = {
        'all': '--all ',
        'patch': '--patch ',
        'message': '--message="',
        'allow empty message': '--allow-empty-message ',
        }
commit_option_rule = RuleRef(name='commit_option', rule=GitCommitOptionRule())
commit_option_rules = Repetition(commit_option_rule, min=1, max=10, name='commit_options')


class GitCommitRule(CompoundRule):
    spec = 'commit [<commit_options>]'
    extras = [commit_option_rules]
git_commit_rule = RuleRef(name='commit_rule', rule=GitCommitRule())


git_command_rule = Alternative(name='command', children=[
    git_add_rule,
    git_commit_rule,
])


class GitRule(CompoundRule):
    spec = 'git <command>'
    extras = [git_command_rule]



git_context = aenea.AeneaContext(
    ProxyAppContext(executable='gnome-terminal'),
    AppContext(executable='cmd.exe')
)
git_grammar = Grammar('git', context=git_context)
git_grammar.add_rule(GitRule())
git_grammar.load()


def unload():
    global git_grammar
    if git_grammar:
        git_grammar.unload()
    git_grammar = None
