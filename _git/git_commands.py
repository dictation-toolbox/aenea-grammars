from aenea import (
    Key,
    Text,
)


def all_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .double_option(['all'])
        .option('dot|point', '.')
        .build(),

        GitCommandRuleBuilder(name='commit', base_options=[Text('-v ')])
        .double_option(['all', 'amend'])
        .option('dot|point', '.')
        .option(
            # NOTE: The user can only say the message option last
            # NOTE 2: This grammar does not have the capability to write out
            # the commit message
            'message',
            Text('-m ') + Key('squote,squote,left'),
            append_space=False,
        )
        .build(),
    ]
