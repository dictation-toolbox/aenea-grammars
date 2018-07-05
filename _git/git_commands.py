from aenea import Text

'''
NOTE: Not all possible commands and options are available in this grammar.
NatLink puts a limit on how complex the grammar can get, and some commands had
to be removed. If you feel like there is something missing here, feel free to
add stuff back and make a pull request.

NOTE 2: Lists of options were grepped from the Git help pages using a bash
script. These have been marked with the comment 'Generated'. Some of these
generated lists are too long, so had to be shortened (see note above). You can
find the script here in case you find it useful
https://gist.github.com/dylan-chong/ecf701b1a623c9f2ccb78cbb5db700c6 . Ideally,
when adding a new command, just add the options that are commonly used.
'''


# Common refs for convenience. The user will still have to type out most branch
# and remote names themselves
_COMMON_BRANCH_NAMES = ['master', 'develop', 'HEAD']
_COMMON_REMOTE_NAMES = ['origin', 'upstream']


def _add_common_refs(rule_builder):
    for remote in _COMMON_REMOTE_NAMES:
        for branch in _COMMON_BRANCH_NAMES:
            rule_builder.smart_options([remote + '/' + branch])

    rule_builder.smart_options(_COMMON_BRANCH_NAMES)
    rule_builder.smart_options(_COMMON_REMOTE_NAMES)

    # TODO Implement this properly in the git grammar
    rule_builder.option('stash at [zero]', 'stash@{0}')


def all_commands(GitCommandRuleBuilder):
    return (
        common_commands(GitCommandRuleBuilder)
        + extra_commands(GitCommandRuleBuilder)
    )


def common_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_options([
            '--',
            '--all',
            '--force',
            '--patch',
            '--update',
            '.',
        ])
        .build(),

        GitCommandRuleBuilder(name='bisect')
        .smart_options([
            'bad',
            'good',
            'log',
            'new',
            'next',
            'old',
            'replay',
            'reset',
            'run',
            'skip',
            'start',
        ])
        .build(),

        GitCommandRuleBuilder(name='branch')
        .convenience_option('easy all', '--verbose --verbose --all')
        .apply(_add_common_refs)
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
        .apply(_add_common_refs)
        .option('branch|be', '-b')
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
        .smart_options(['.'])
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
        .apply(_add_common_refs)
        .smart_options([
            '--',
            '--cached',
            '--staged',
            '--stat',
            '.',
        ])
        .build(),

        GitCommandRuleBuilder(name='fetch')
        .convenience_option('easy all', '--all --tags --prune')
        .apply(_add_common_refs)
        .smart_options([
            '--all',
            '--force',
            '--prune',
            '--tags',
            '--verbose',
            '--[no-]recurse-submodules',
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

        GitCommandRuleBuilder(name='log')
        .convenience_option(
            'easy all',
            '--graph --all --oneline --topo-order',
        )
        .convenience_option(
            'easy oneline',
            '--graph --oneline --topo-order',
        )
        .apply(_add_common_refs)
        .smart_options([
            # Not generated because there are too many options
            '--',
            '--all',
            '--author-date-order',
            '--date-order',
            '--decorate',
            '--first-parent',
            '--graph',
            '--oneline',
            '--patch',
            '--stat',
            '--topo-order',
            '--word-diff',
        ])
        .build(),

        GitCommandRuleBuilder(name='merge')
        .apply(_add_common_refs)
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

        GitCommandRuleBuilder(name='mv', alias='move|em-vee')
        .smart_options([
            # Generated:
            '--dry-run', '--force', '--verbose',
        ])
        .build(),

        GitCommandRuleBuilder(name='pull')
        .convenience_option('easy push', '--rebase && git push')
        .apply(_add_common_refs)
        .smart_options([
            '--force',
            '--rebase',
        ])
        .build(),

        GitCommandRuleBuilder(name='push')
        .apply(_add_common_refs)
        .smart_options([
            '--all',
            '--delete',
            '--tags',
            '--force',
            '--set-upstream',
        ])
        .build(),

        GitCommandRuleBuilder(name='rebase')
        .apply(_add_common_refs)
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
        .apply(_add_common_refs)
        .smart_options([
            # Generated:
            '--', '--amend', '--cached', '--hard', '--keep', '--merge',
            '--mixed', '--option', '--quiet', '--soft',
        ])
        .build(),

        GitCommandRuleBuilder(name='rm', alias='remove|are-em')
        .smart_options([
            # Generated:
            '--', '--cached', '--diff-filter=', '--dry-run', '--force',
            '--ignore-unmatch', '--name-only', '--quiet',
        ])
        .build(),

        GitCommandRuleBuilder(name='show')
        .apply(_add_common_refs)
        .smart_options([
            '--',
            '--stat',
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


def extra_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='apply')
        .smart_options([
            # Generated:
            '--3way', '--allow-binary-replacement', '--apply', '--binary',
            '--build-fake-ancestor=', '--cached', '--check', '--directory=',
            '--exclude=', '--ignore-space-change', '--ignore-whitespace',
            '--inaccurate-eof', '--include=', '--index', '--no-add',
            '--numstat', '--recount', '--reject', '--reverse', '--stat',
            '--summary', '--unidiff-zero', '--unsafe-paths', '--verbose',
            '--whitespace=',
        ])
        .build(),

        GitCommandRuleBuilder(name='blame')
        .smart_options([
            # Generated:
            '--', '--[no-]progress', '--abbrev=', '--contents', '--date',
            '--diff-filter=', '--encoding=', '--incremental',
            '--line-porcelain', '--porcelain', '--pretty=', '--reverse',
            '--root', '--score-debug', '--show-email', '--show-name',
            '--show-number', '--show-stats', '--since=',
        ])
        .build(),

        GitCommandRuleBuilder(name='cherry-pick')
        .apply(_add_common_refs)
        .smart_options([
            # Generated:
            '--abort', '--allow-empty', '--allow-empty-message', '--continue',
            '--edit', '--ff', '--gpg-sign', '--keep-redundant-commits',
            '--mainline', '--merge', '--no-commit', '--quit', '--signoff',
            '--strategy-option=', '--strategy=',
        ])
        .build(),

        GitCommandRuleBuilder(name='config')
        .smart_options([
            '--global',
        ])
        .build(),

        GitCommandRuleBuilder(name='ls-files', alias='(el-es|list) files')
        .smart_options([
            '--no-empty-directory',
        ])
        .build(),

        GitCommandRuleBuilder(name='merge-base')
        .apply(_add_common_refs)
        .smart_options([
            # Generated:
            '--all', '--fork-point', '--independent', '--is-ancestor',
            '--octopus', '--onto', '--verify',
        ])
        .build(),

        GitCommandRuleBuilder(name='remote')
        .smart_options(_COMMON_REMOTE_NAMES)
        .smart_options([
            'add',
            'remove',
            'rename',
            'set-url',
            'show',
        ])
        .smart_options([
            '--verbose'
        ])
        .build(),

        GitCommandRuleBuilder(name='revert')
        .apply(_add_common_refs)
        .smart_options([
            # Generated:
            '--abort', '--continue', '--edit', '--gpg-sign', '--mainline',
            '--no-commit', '--no-edit', '--quit', '--signoff',
            '--strategy-option=', '--strategy=',
        ])
        .build(),

        GitCommandRuleBuilder(name='shortlog')
        .apply(_add_common_refs)
        .smart_options([
            # Generated:
            '--committer', '--email', '--format', '--numbered', '--pretty=',
            '--summary',
        ])
        .build(),

        GitCommandRuleBuilder(name='stash')
        .smart_options([
            'apply', 'branch', 'clear', 'create', 'drop', 'list', 'pop',
            'push', 'save', 'save', 'show', 'store',
        ])
        .smart_options([
            # Generated:
            '--grep=', '--keep-index', '--merges', '--no-walk', '--patch',
            '--soft', '--unreachable',
        ])
        .build(),

        GitCommandRuleBuilder(name='submodule')
        .smart_options([
            'absorbgitdirs', 'add', 'deinit', 'foreach', 'init', 'status',
            'summary', 'sync', 'update',
        ])
        .smart_options([
            # Generated:
            '--', '--[no-]recommend-shallow', '--all', '--branch', '--cached',
            '--checkout', '--depth', '--files', '--force', '--init', '--jobs',
            '--merge', '--name', '--no-fetch', '--quiet', '--rebase',
            '--recursive', '--reference', '--remote', '--summary-limit',
        ])
        .build(),

        GitCommandRuleBuilder(name='worktree')
        .apply(_add_common_refs)
        .smart_options([
            'add', 'list', 'lock', 'move', 'prune', 'remove', 'unlock',
        ])
        .smart_options([
            # Generated:
            '--[no-]checkout', '--detach', '--dry-run', '--expire', '--force',
            '--lock', '--porcelain', '--reason', '--verbose',
        ])
        .build(),
    ]
