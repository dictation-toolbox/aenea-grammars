from aenea import Text

'''
Useful bash script for grabbing all of the options from all help pages:

::

    commands=`git help | egrep '^\s{3}\w' | awk '{ print $1 }'`
    # TODO Continue this


    # TODO tidy this
    git help <SOME_COMMAND> \
    git help checkout \
      | tr " " "\n" \
      | egrep '^\--.*$' \
      | egrep -v '/' \
      | egrep -v '\-{3,}' \
      | perl -pe 's/[^\w=\n\[\]<>-]//' \
      | perl -pe 's/([^=]+)=.*/\1=/' \
      | perl -pe 's/<.*>//' \
      | perl -pe 's/^\[(.*)\]$/\1/' \
      | sort \
      | uniq
      | uniq \
      | perl -pe "s/(.*)(\n?)/'\1', /"

NOTE: Most of the Git options in this file have been generated using the above
script. These have been marked with a comment saying 'Generated'.
'''


# TODO common branch name and a boat names

def all_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_options(['.'])
        .smart_options([
            # Generated:
            '--', '--all,', '--chmod', '--dry-run', '--dry-run.', '--edit',
            '--force', '--ignore-errors', '--ignore-missing',
            '--ignore-removal', '--intent-to-add', '--interactive', '--no-all',
            '--no-all,', '--no-ignore-removal', '--no-warn-embedded-repo',
            '--patch', '--refresh', '--update', '--verbose',
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
