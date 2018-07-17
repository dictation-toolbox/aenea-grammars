from aenea import Text

'''
NOTE: Not all possible commands and options are available in this grammar.
NatLink puts a limit on how complex the grammar can get, and so the commands
and options listed below are just the ones that should be useful for most
people. If you feel like there is something missing here, feel free to make a
pull request.
'''

# TODO remove unneeded commands EVERYWHERE and remove the Generateed commands
# TODO stash nums
# TODO git flow?

# Common refs for convenience. The user will still have to type out most branch
# and remote names themselves
_COMMON_BRANCH_NAMES = ['master', 'develop']
_COMMON_REMOTE_NAMES = ['origin', 'upstream']


def _add_common_refs(rule_builder):
    # TODO This create a lot of mappings, making the grammar complex. Move this
    # into the grammar itself and have an option to enable it
    for remote in _COMMON_REMOTE_NAMES:
        for branch in _COMMON_BRANCH_NAMES:
            rule_builder.smart_options([remote + '/' + branch])

    rule_builder.smart_options(_COMMON_BRANCH_NAMES)
    rule_builder.smart_options(_COMMON_REMOTE_NAMES)

    # See https://github.com/junegunn/fzf/wiki/Examples#git
    # TODO Delete this when submitting the pull request
    rule_builder.option('select branch', '`fbr`')


def all_commands(GitCommandRuleBuilder):
    return (
        common_commands(GitCommandRuleBuilder)
        + extra_commands(GitCommandRuleBuilder)
    )


def common_commands(GitCommandRuleBuilder):
    return [
        GitCommandRuleBuilder(name='add')
        .smart_options(['.'])
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
        .smart_options(
            # Generated from the output of `git bisect` without any arguments
            ('help|start|bad|good|new|old|terms|skip|next|reset|visualize|'
             + 'replay|log|run').split('|')
        )
        .smart_options([
            # Generated:
            '--', '--hard', '--no-checkout', '--no-commit', '--not',
            '--objects', '--stat', '--stdout', '--term-bad', '--term-new',
            '--term-old',
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
        .smart_options(['.'])
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
        .convenience_option('easy all', '--all --tags --prune')
        .apply(_add_common_refs)
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
        .apply(_add_common_refs)
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
            # Generated:
            '--', '--[no-]includes', '--[no-]recurse-submodules', '--add',
            '--all', '--attach', '--auto', '--blob', '--bool', '--bool-or-int',
            '--branch', '--cc', '--edit', '--file', '--get', '--get-all',
            '--get-color', '--get-colorbool', '--get-regexp', '--get-urlmatch',
            '--git-dir', '--global', '--ignore-submodules',
            '--ignore-submodules=', '--int', '--interactive',
            '--interactive).', '--list', '--local', '--local-user',
            '--name-only', '--negotiate', '--no-branch', '--no-index',
            '--no-short', '--no-tags', '--not', '--ntlm', '--null',
            '--numbered', '--path', '--pretty=', '--receive-pack',
            '--remove-section', '--rename-section', '--replace-all',
            '--scissors', '--short', '--show-origin', '--stat',
            '--summary-limit', '--system', '--tags', '--to', '--unset',
            '--unset-all', '--upload-pack', '--work-tree',
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
