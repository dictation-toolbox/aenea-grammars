from aenea import Text

'''
Useful bash script for grabbing all of the options from all help pages:

::
    #!/bin/bash
    options_for_command() {
        # Just change copy and change the $1 in the statement here if you want
        # to just regenerate the options for a single command
        git help $1 \
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
        echo ".build(),"
        echo
    }

    # Note: This doesn't generate all the commands. Just the common ones.
    # You have to manually run builder_code_for_command on other git commands
    # to generate the builder code for them.
    commands=`git help | egrep '^\s{3}\w' | awk '{ print $1 }' | sort`

    for command in $commands; do
        builder_code_for_command $command
    done \
        | less

NOTE: Most of the Git options in this file have been generated using the above
script. These have been marked with a comment saying 'Generated'.
'''


# TODO common branch name and a boat names
# TODO simplified bash script above because most people want need to generate
# all of the commands
# TODO stash comands
# TODO More convenience commands

def all_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_option('.')
        .smart_options([
            # Generated:
            '--', '--[no-]ignore-removal', '--all', '--chmod=', '--dry-run',
            '--edit', '--force', '--ignore-errors', '--ignore-missing',
            '--ignore-removal', '--intent-to-add', '--interactive', '--no-all',
            '--no-ignore-removal', '--no-warn-embedded-repo', '--patch',
            '--refresh', '--update', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='bisect')
        .smart_options([
            # Generated:
            '--', '--hard', '--no-checkout', '--no-commit', '--not',
            '--objects', '--stat', '--stdout', '--term-bad', '--term-new',
            '--term-old',
        ])
        .build(),

        GitCommandRuleBuilder(name='branch')
        .smart_options([
            # Generated:
            '--abbrev=', '--all', '--color', '--column', '--contains',
            '--copy', '--create-reflog', '--delete', '--edit-description',
            '--force', '--format', '--ignore-case', '--list', '--merged',
            '--move', '--no-abbrev', '--no-color', '--no-column',
            '--no-contains', '--no-merged', '--no-track', '--points-at',
            '--quiet', '--remotes', '--set-upstream', '--set-upstream-to=',
            '--sort=', '--track', '--unset-upstream', '--verbose',
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

        GitCommandRuleBuilder(name='clone')
        .smart_options([
            # Generated:
            '--[no-]shallow-submodules', '--[no-]single-branch', '--bare',
            '--branch', '--config', '--depth', '--dissociate', '--jobs',
            '--local', '--mirror', '--no-checkout', '--no-hardlinks',
            '--no-tags', '--origin', '--progress', '--quiet',
            '--recurse-submodules', '--reference', '--reference[-if-able]',
            '--separate-git-dir=', '--shallow-exclude=', '--shallow-since=',
            '--shared', '--template=', '--upload-pack', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='commit', base_options=[Text(' -v')])
        .smart_option('.')
        .smart_options([
            # Generated:
            '--', '--all', '--allow-empty', '--allow-empty-message', '--amend',
            '--author=', '--branch', '--cleanup=', '--date=', '--dry-run',
            '--edit', '--file=', '--fixup', '--fixup=', '--gpg-sign',
            '--include', '--interactive', '--long', '--message=', '--no-edit',
            '--no-gpg-sign', '--no-post-rewrite', '--no-status', '--no-verify',
            '--null', '--only', '--patch', '--porcelain', '--quiet',
            '--reedit-message=', '--reset-author', '--reuse-message=',
            '--short', '--signoff', '--soft', '--squash', '--squash=',
            '--status', '--template=', '--untracked-files', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='diff')
        .smart_option('.')
        .smart_options([
            # Generated:
            '--', '--abbrev', '--base', '--binary', '--cached', '--cached.',
            '--cc', '--check', '--color', '--color-moved', '--color-words',
            '--combined', '--diff-filter=', '--dirstat', '--dst-prefix=',
            '--exit-code', '--ext-diff', '--find-copies',
            '--find-copies-harder', '--find-renames', '--full-index',
            '--function-context', '--git', '--histogram', '--ignore-all-space',
            '--ignore-blank-lines', '--ignore-space-at-eol',
            '--ignore-space-change', '--ignore-submodules',
            '--indent-heuristic', '--inter-hunk-context=',
            '--irreversible-delete', '--ita-invisible-in-index',
            '--line-prefix=', '--minimal', '--name-only', '--name-status',
            '--no-color', '--no-ext-diff', '--no-indent-heuristic',
            '--no-index', '--no-patch', '--no-prefix', '--no-renames',
            '--no-textconv', '--numstat', '--ours', '--patch',
            '--patch-with-raw', '--patch-with-stat', '--patience',
            '--pickaxe-all', '--pickaxe-regex', '--quiet', '--raw',
            '--relative', '--shortstat', '--src-prefix=', '--staged', '--stat',
            '--submodule', '--summary', '--text', '--textconv', '--theirs',
            '--unified=', '--word-diff', '--word-diff-regex=',
            '--ws-error-highlight=',
        ])
        .build(),

        GitCommandRuleBuilder(name='fetch')
        .smart_options([
            # Generated:
            '--[no-]recurse-submodules', '--all', '--append', '--deepen=',
            '--depth', '--depth=', '--dry-run', '--force', '--ipv4', '--ipv6',
            '--jobs=', '--keep', '--local', '--mirror', '--multiple',
            '--no-recurse-submodules', '--no-tags', '--progress', '--prune',
            '--quiet', '--recurse-submodules', '--recurse-submodules-default=',
            '--refmap=', '--shallow-exclude=', '--shallow-since=',
            '--submodule-prefix=', '--tags', '--unshallow', '--update-head-ok',
            '--update-shallow', '--upload-pack', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='grep')
        .smart_options([
            # Generated:
            '--', '--after-context', '--all-match', '--and', '--basic-regexp',
            '--before-context', '--break', '--cached', '--color', '--context',
            '--count', '--exclude-standard', '--extended-regexp',
            '--files-with-matches', '--files-without-match', '--fixed-strings',
            '--full-name', '--function-context', '--heading', '--ignore-case',
            '--invert-match', '--line-number', '--max-depth', '--name-only',
            '--no-color', '--no-exclude-standard', '--no-index',
            '--no-textconv', '--not', '--null', '--open-files-in-pager',
            '--or', '--perl-regexp', '--quiet', '--recurse-submodules',
            '--show-function', '--text', '--textconv', '--threads',
            '--untracked', '--word-regexp',
        ])
        .build(),

        GitCommandRuleBuilder(name='init')
        .smart_options([
            # Generated:
            '--bare', '--quiet', '--separate-git-dir', '--separate-git-dir=',
            '--shared', '--template=',
        ])
        .build(),

        GitCommandRuleBuilder(name='log', base_options=[Text(' --graph')])
        .smart_options([
            # Generated:
            '--', '--[no-]standard-notes', '--abbrev', '--abbrev-commit',
            '--after=', '--all', '--all-match', '--ancestry-path',
            '--author-date-order', '--author=', '--basic-regexp', '--before=',
            '--binary', '--bisect', '--boundary', '--branches', '--cached.',
            '--cc', '--check', '--cherry', '--cherry-mark', '--cherry-pick',
            '--children', '--color', '--color-moved', '--color-words',
            '--combined', '--committer=', '--date-order', '--date=',
            '--decorate', '--dense', '--diff-filter=', '--dirstat',
            '--do-walk', '--dst-prefix=', '--encoding=', '--exclude=',
            '--exit-code', '--expand-tabs', '--expand-tabs=', '--ext-diff',
            '--extended-regexp', '--find-copies', '--find-copies-harder',
            '--find-renames', '--first-parent', '--fixed-strings', '--follow',
            '--format=', '--full-diff', '--full-history', '--full-index',
            '--function-context', '--git', '--glob=', '--graph',
            '--grep-reflog=', '--grep=', '--histogram', '--ignore-all-space',
            '--ignore-blank-lines', '--ignore-missing',
            '--ignore-space-at-eol', '--ignore-space-change',
            '--ignore-submodules', '--indent-heuristic',
            '--inter-hunk-context=', '--invert-grep', '--irreversible-delete',
            '--ita-invisible-in-index', '--left-only', '--left-right',
            '--line-prefix=', '--log-size', '--max-count=', '--max-parents=',
            '--merge', '--merges', '--min-parents=', '--minimal',
            '--name-only', '--name-status', '--no-abbrev',
            '--no-abbrev-commit', '--no-color', '--no-decorate',
            '--no-expand-tabs', '--no-ext-diff', '--no-indent-heuristic',
            '--no-max-parents', '--no-merges', '--no-min-parents',
            '--no-notes', '--no-patch', '--no-prefix', '--no-renames',
            '--no-textconv', '--no-walk', '--not', '--notes', '--notes=',
            '--numstat', '--oneline', '--parents', '--patch',
            '--patch-with-raw', '--patch-with-stat', '--patience',
            '--perl-regexp', '--pickaxe-all', '--pickaxe-regex', '--pretty',
            '--pretty=', '--raw', '--reflog', '--regexp-ignore-case',
            '--relative', '--relative-date', '--remotes', '--remove-empty',
            '--reverse', '--right-only', '--shortstat', '--show-linear-break',
            '--show-notes', '--show-signature', '--simplify-by-decoration',
            '--simplify-merges', '--since=', '--single-worktree', '--skip=',
            '--source', '--sparse', '--src-prefix=', '--stat', '--stdin',
            '--submodule', '--summary', '--tags', '--text', '--textconv',
            '--topo-order', '--unified=', '--until=', '--use-mailmap',
            '--walk-reflogs', '--word-diff', '--word-diff-regex=',
            '--ws-error-highlight=',
        ])
        .build(),

        GitCommandRuleBuilder(name='merge')
        .smart_options([
            # Generated:
            '--[no-]rerere-autoupdate', '--abort',
            '--allow-unrelated-histories', '--commit', '--continue', '--edit',
            '--ff', '--ff-only', '--gpg-sign', '--log', '--no-commit',
            '--no-edit', '--no-ff', '--no-log', '--no-progress', '--no-squash',
            '--no-stat', '--no-summary', '--no-verify-signatures',
            '--progress', '--quiet', '--signoff', '--squash', '--stat',
            '--strategy-option=', '--strategy=', '--summary', '--verbose',
            '--verify-signatures',
        ])
        .build(),

        GitCommandRuleBuilder(name='mv')
        .smart_options([
            # Generated:
            '--dry-run', '--force', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='pull')
        .smart_options([
            # Generated:
            '--[no-]recurse-submodules', '--all',
            '--allow-unrelated-histories', '--append', '--autostash',
            '--commit', '--deepen=', '--depth', '--depth=', '--edit', '--ff',
            '--ff-only', '--force', '--gpg-sign', '--ipv4', '--ipv6', '--keep',
            '--local', '--log', '--no-autostash', '--no-commit', '--no-edit',
            '--no-ff', '--no-log', '--no-rebase', '--no-squash', '--no-stat',
            '--no-summary', '--no-tags', '--no-verify-signatures',
            '--progress', '--quiet', '--rebase', '--recurse-submodules',
            '--shallow-exclude=', '--shallow-since=', '--squash', '--stat',
            '--strategy-option=', '--strategy=', '--summary', '--unshallow',
            '--update-head-ok', '--update-shallow', '--upload-pack',
            '--verbose', '--verify-signatures',
        ])
        .build(),

        GitCommandRuleBuilder(name='push')
        .smart_options([
            # Generated:
            '--[no-]atomic', '--[no-]force-with-lease', '--[no-]signed',
            '--[no-]thin', '--[no-]verify', '--all', '--amend', '--delete',
            '--dry-run', '--exec=', '--follow-tags', '--force',
            '--force-with-lease', '--force-with-lease=', '--ipv4', '--ipv6',
            '--local', '--mirror', '--no-recurse-submodules', '--no-verify',
            '--porcelain', '--progress', '--prune', '--push-option', '--quiet',
            '--rebase,', '--receive-pack=', '--recurse-submodules=', '--repo=',
            '--set-upstream', '--signed=', '--tags', '--thin', '--verbose',
            '--verify',
        ])
        .build(),

        GitCommandRuleBuilder(name='rebase')
        .smart_options([
            # Generated:
            '--abort', '--autosquash', '--autostash',
            '--committer-date-is-author-date', '--continue', '--edit-todo',
            '--exec', '--force-rebase', '--fork-point', '--gpg-sign',
            '--ignore-date', '--ignore-whitespace', '--interactive',
            '--keep-empty', '--merge', '--no-autosquash', '--no-autostash',
            '--no-ff', '--no-fork-point', '--no-stat', '--no-verify', '--onto',
            '--preserve-merges', '--quiet', '--quit', '--root', '--signoff',
            '--skip', '--stat', '--strategy-option=', '--strategy=',
            '--verbose', '--verify', '--whitespace=',
        ])
        .build(),

        GitCommandRuleBuilder(name='reset')
        .smart_options([
            # Generated:
            '--', '--amend', '--cached', '--hard', '--keep', '--merge',
            '--mixed', '--option', '--quiet', '--soft',
        ])
        .build(),

        GitCommandRuleBuilder(name='rm')
        .smart_options([
            # Generated:
            '--', '--cached', '--diff-filter=', '--dry-run', '--force',
            '--ignore-unmatch', '--name-only', '--quiet',
        ])
        .build(),

        GitCommandRuleBuilder(name='show')
        .smart_options([
            # Generated:
            '--', '--[no-]standard-notes', '--abbrev', '--abbrev-commit',
            '--binary', '--cached.', '--cc', '--check', '--color',
            '--color-moved', '--color-words', '--combined', '--date=',
            '--decorate', '--diff-filter=', '--dirstat', '--dst-prefix=',
            '--encoding=', '--exit-code', '--expand-tabs', '--expand-tabs=',
            '--ext-diff', '--find-copies', '--find-copies-harder',
            '--find-renames', '--format=', '--full-index',
            '--function-context', '--git', '--histogram', '--ignore-all-space',
            '--ignore-blank-lines', '--ignore-space-at-eol',
            '--ignore-space-change', '--ignore-submodules',
            '--indent-heuristic', '--inter-hunk-context=',
            '--irreversible-delete', '--ita-invisible-in-index',
            '--line-prefix=', '--minimal', '--name-only', '--name-only.',
            '--name-status', '--no-abbrev', '--no-abbrev-commit', '--no-color',
            '--no-expand-tabs', '--no-ext-diff', '--no-indent-heuristic',
            '--no-notes', '--no-patch', '--no-prefix', '--no-renames',
            '--no-textconv', '--notes', '--notes=', '--numstat', '--oneline',
            '--patch', '--patch-with-raw', '--patch-with-stat', '--patience',
            '--pickaxe-all', '--pickaxe-regex', '--pretty', '--pretty=',
            '--raw', '--relative', '--shortstat', '--show-notes',
            '--show-signature', '--src-prefix=', '--stat', '--submodule',
            '--summary', '--text', '--textconv', '--unified=', '--word-diff',
            '--word-diff-regex=', '--ws-error-highlight=',
        ])
        .build(),

        GitCommandRuleBuilder(name='status')
        .smart_options([
            # Generated:
            '--', '--branch', '--column', '--ignore-submodules',
            '--ignore-submodules=', '--ignored', '--long', '--no-column',
            '--porcelain', '--short', '--show-stash', '--summary-limit',
            '--untracked-files', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='tag')
        .smart_options([
            # Generated:
            '--annotate', '--cleanup=', '--color', '--column', '--contains',
            '--create-reflog', '--delete', '--file=', '--force',
            '--ignore-case', '--list', '--local-user=', '--merged',
            '--message=', '--no-column', '--no-contains', '--no-merged',
            '--points-at', '--sign', '--sort=', '--verify',
        ])
        .build(),
    ]
