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
    Terminology:
    - name: name to give to the rule (to make it unique), acts as a default
      alias and text
    - alias: what to say to match this command
    - text: what gets typed out when this command gets matched

    Example things you can say:
    - git <alias>
    - git <alias> <option1> <option2>
    - git help <alias>
    '''
    def __init__(
            self,
            name,
            options,
            alias=None,
            text=None,
            default_options=[],
    ):
        if alias is None:
            alias = name
        if text is None:
            text = name

        self.default_options = default_options
        self.text = text

        super(GitCommandRule, self).__init__(
            name=name,
            spec='[help] {} <options>'.format(alias),
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

        output_text = Text('git {}{} '.format(
            'help ' if help else '',
            self.text,
        ))

        if help:
            options = option_values
        else:
            options = self.default_options + option_values
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

    def option(self, alias, text, append_space=True):
        if alias in self.data:
            raise ValueError('{} is already in {}'.format(alias, self.data))

        result_text = text
        if isinstance(result_text, basestring):
            result_text = Text(text)
        if append_space:
            result_text += Text(' ')

        self.data['options'][alias] = result_text
        return self

    def build(self):
        return RuleRef(
            name=self.data['name'],
            rule=GitCommandRule(**self.data),
        )


class GitRule(CompoundRule):
    def __init__(self):
        # TODO get help
        super(GitRule, self).__init__(
            spec='git [<command_with_options>] [<enter>] [<cancel>]',
            extras=[
                Alternative(
                    name='command_with_options',
                    children=all_commands(),
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


def all_commands():
    return [
        GitCommandRuleBuilder(name='add')
        .double_option(['all'])
        .option('dot|point', '.')
        .build(),

        GitCommandRuleBuilder(name='commit', default_options=[Text('-v ')])
        .double_option(['all', 'amend'])
        .option('dot|point', '.')
        .option(
            # NOTE: The user can only say the message option last
            # NOTE 2: This grammar does not have the capability to write out
            # the commit message
            'message',
            Text('-m ') + Key('dquote,dquote,left'),
            append_space=False,
        )
        .build(),
    ]


load()
