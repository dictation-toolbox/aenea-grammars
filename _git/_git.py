# NOTE: You need to copy this file and git_commands.py to MacroSystem
import git_commands

import aenea.config
import aenea.configuration
import re

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


def wrap_options(options):
    return {
        # wrap value which is a Text, to prevent it from being
        # executed automatically
        key: (value,)
        for key, value in options.iteritems()
    }


def unwrap_values(values):
    # see wrap_options()
    return [value for value, in values]


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
            alias=None,
            base_options=[],
    ):
        alias = alias or name
        self.base_options = base_options

        super(GitCommandRule, self).__init__(
            name=name,
            spec='[help] ({}) <options>'.format(alias),
            extras=[Repetition(
                name='options',
                min=0,
                max=10,
                child=RuleRef(MappingRule(
                    name=name + '_options',
                    mapping=wrap_options(options),
                )),
            )],
        )

    def value(self, node):
        sequence_values = node.children[0].children[0].value()

        help = not not sequence_values[0]
        option_values = unwrap_values(sequence_values[2])

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

    def option(self, alias, option, append_space=True):
        alias = alias.strip()

        if alias in self.data['options']:
            return

        result_text = option
        if isinstance(result_text, basestring):
            result_text = Text(option)
        if append_space:
            result_text = Text(' ') + result_text

        self.data['options'][alias] = result_text
        return self

    def _smart_option(self, option, **keyword_arguments):
        '''
        Accepts a variety of inputs, and converts them into an appropriate
        format for dictation. For example, all of the following are valid:

        :code:`['.', '-', '--', 'some-option', '--another-option',
        '--[no-]using-the-thing', 'something/else']`

        Note that the user must say 'slash' if there is a '/' in the option.
        '''

        optional_pattern = r'-(.*)\[(.+)?\](.*)'

        if option == '.':
            alias = 'dot|point'
        elif re.match(r'^-+$', option):
            alias = 'dash ' * len(option)
        elif re.match(optional_pattern, option):
            # For example, option = '--[no-]progress'
            return self.smart_options([
                # For example, '--no-progress'
                re.sub(optional_pattern, r'-\1\2\3', option, count=1),
                # For example, '--progress'
                re.sub(optional_pattern, r'-\1\3', option, count=1),
            ], **keyword_arguments)
        else:
            alias = option
            alias = re.sub(r'/', ' slash ', alias)
            alias = re.sub(r'[^a-zA-Z0-9]', ' ', alias)

        return self.option(alias, option, **keyword_arguments)

    def smart_options(self, options, **keyword_arguments):
        '''See documentation for _smart_option()'''

        for option in options:
            self._smart_option(option, **keyword_arguments)

        return self

    convenience_option = option

    def apply(self, function):
        function(self)
        return self

    def build(self):
        return RuleRef(
            name=self.data['name'],
            rule=GitCommandRule(**self.data),
        )


class GitRule(CompoundRule):
    def __init__(self):
        commands = git_commands.all_commands(GitCommandRuleBuilder)
        spec = '[<cancel>] git [<command_with_options>] [<enter>] [<cancel>]'

        super(GitRule, self).__init__(
            spec=spec,
            extras=[
                RuleRef(name='cancel', rule=MappingRule(
                    name='cancel',
                    mapping={'cancel [last]': Key('c-c')},
                )),
                Alternative(
                    name='command_with_options',
                    children=commands,
                ),
                RuleRef(name='enter', rule=MappingRule(
                    name='enter',
                    mapping={'enter': Key('enter')},
                )),
            ],
        )

    def _process_recognition(self, node, extras):
        for name in ['cancel', 'command_with_options', 'enter']:
            executable = extras.get(name)
            if executable:
                executable.execute()


load()
