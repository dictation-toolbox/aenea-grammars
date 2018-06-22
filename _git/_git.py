import aenea.config
import aenea.configuration
import re
import git_commands

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

# TODO What is aenea.configuration.make_grammar_commands


def load():
    global git_grammar
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


class GitCommandRule(CompoundRule):
    '''
    Example things you can say:
    - git <name>
    - git <name> <option1> <option2>
    - git help <name>
    '''
    def __init__(
            self,
            name,
            options,
            base_options=[],
    ):
        self.base_options = base_options

        super(GitCommandRule, self).__init__(
            name=name,
            spec='[help] {} <options>'.format(name),
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
        sequence_values = node.children[0].children[0].value()

        help = not not sequence_values[0]
        option_values = sequence_values[2]

        output_text = Text('git {}{}'.format(
            'help ' if help else '',
            self.name,
        ))

        if help:
            options = option_values
        else:
            options = self.base_options + option_values
        for option in options:
            output_text += option

        return output_text


class GitCommandRuleBuilder:
    def __init__(self, **data):
        if 'options' not in data:
            data['options'] = dict()
        self.data = data

    def double_option(self, alias, **keyword_arguments):
        '''For example, "--alias".'''
        if isinstance(alias, (list, tuple)):
            aliases = alias
        else:
            aliases = [alias]

        for al in aliases:
            self.option(al, '--' + al, **keyword_arguments)

        return self

    def option(self, alias, option, append_space=True):
        if alias in self.data:
            raise ValueError('{} is already in {}'.format(alias, self.data))

        result_text = option
        if isinstance(result_text, basestring):
            result_text = Text(option)
        if append_space:
            result_text = Text(' ') + result_text

        self.data['options'][alias] = result_text
        return self

    def smart_options(self, options, **keyword_arguments):
        for option in options:
            if option == '.':
                alias = 'dot|point'
            elif re.match(r'^-+$', option):
                alias = 'dash ' * len(option)
            else:
                alias = re.sub(r'[^a-zA-Z0-9]', ' ', option)

            alias = alias.strip()
            self.option(alias, option, **keyword_arguments)

        return self

    def build(self):
        return RuleRef(
            name=self.data['name'],
            rule=GitCommandRule(**self.data),
        )


class GitRule(CompoundRule):
    def __init__(self):
        commands = git_commands.all_commands(GitCommandRuleBuilder)

        super(GitRule, self).__init__(
            spec='git [<command_with_options>] [<enter>] [<cancel>]',
            extras=[
                Alternative(
                    name='command_with_options',
                    children=commands,
                ),
                RuleRef(name='enter', rule=MappingRule(
                    name='enter',
                    mapping={'enter': Key('enter')},
                )),
                RuleRef(name='cancel', rule=MappingRule(
                    name='cancel',
                    mapping={'cancel': Key('c-c')},
                )),
            ],
        )

    def _process_recognition(self, node, extras):
        def execute(name):
            executable = extras.get(name)
            if executable:
                executable.execute()

        for name in ['command_with_options', 'enter', 'cancel']:
            execute(name)


load()
