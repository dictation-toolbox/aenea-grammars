from aenea import Text

'''
Useful bash script for grabbing all of the options from all help pages:

::
    #!/bin/bash
    options_for_command() {
        git help $1 \
        git help tag \
            | tr " " "\n" \
            | egrep '^\--.*$' \
            | egrep -v '/' \
            | egrep -v '\-{3,}' \
            | egrep -v '{|}' \
            | perl -pe 's/\[=.*\]//' \
            | perl -pe 's/[^\w=\n\[\]<>-]//' \
            | perl -pe 's/([^=]+)=.*/\1=/' \
            | perl -pe 's/<.*>//' \
            | perl -pe 's/^\[(.*)\]$/\1/' \
            | perl -pe 's/^([^\[\]]+)\]+$/\1/' \
            | sort \
            | uniq \
            | perl -pe "s/(.*)(\n?)/'\1', /"
    }

    builder_code_for_command() {
        echo "GitCommandRuleBuilder(name='$command')"
        echo ".smart_options(["
        echo "    # Generated:"
        echo "    `options_for_command $command`"
        echo "])"
        echo ".build()"
        echo
    }

    commands=`git help | egrep '^\s{3}\w' | awk '{ print $1 }' | sort`

    for command in $commands; do
        builder_code_for_command $command
    done \
        | less

NOTE: Most of the Git options in this file have been generated using the above
script. These have been marked with a comment saying 'Generated'.
'''


# TODO common branch name and a boat names
# TODO blame,stash comands

def all_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_option('.')
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
        .smart_option('.')
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

        GitCommandRuleBuilder(name='checkout')
        .smart_options(['.', '-'])
        .smart_options([
            # Generated:
            '--', '--[no-]progress', '--[no-]recurse-submodules',
            '--conflict=', '--detach', '--force', '--ignore-other-worktrees',
            '--ignore-skip-worktree-bits', '--merge',
            '--no-recurse-submodules', '--no-track', '--orphan', '--ours',
            '--patch', '--quiet', '--recurse-submodules', '--theirs',
            '--track',
        ])
        .build(),
    ]
