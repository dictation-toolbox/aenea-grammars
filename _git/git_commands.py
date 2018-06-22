from aenea import Text

'''
Useful bash script for grabbing all of the options from a help page:

::

    git help <SOME_COMMAND> \
      | tr " " "\n" \
      | egrep '^\--.*$' \
      | egrep -v '/' \
      | egrep -v ');?$' \
      | egrep -v '\]' \
      | egrep -v '\-{3,}' \
      | perl -pe 's/\[(.*)\]/\1/' \
      | perl -pe 's/<.*>//' \
      | perl -pe 's/([^=]+)=.*/\1/' \
      | sort \
      | uniq \
      | perl -pe "s/(.*)(\n?)/'\1', /"

NOTE: Most of the Git options in this file have been generated using the above
script. These have been marked with a comment saying 'Generated'.
'''


def all_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_options(['.'])
        .smart_options([
            # Generated:
            # TODO  NEXT
        ])
        .build(),

        GitCommandRuleBuilder(name='commit', base_options=[Text(' -v')])
        .smart_options(['.'])
        .smart_options([
            # Generated:
            '--', '--all', '--allow-empty', '--allow-empty-message', '--amend',
            '--author', '--branch', '--cleanup', '--date', '--dry-run',
            '--edit', '--file', '--fixup', '--include', '--interactive',
            '--long', '--message', '--no-edit', '--no-gpg-sign',
            '--no-post-rewrite', '--no-status', '--no-verify', '--null',
            '--only', '--patch', '--porcelain', '--quiet', '--reedit-message',
            '--reset-author', '--reuse-message', '--short', '--signoff',
            '--soft', '--squash', '--status', '--template', '--verbose',
        ])
        .build(),
    ]
