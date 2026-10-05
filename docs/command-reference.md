# Git command reference lab

> Level 23 · organised by purpose · every command links to the lesson that teaches it · run the practice blocks from
> the course folder (`git-practical-course/`)

This is not a list to memorise. For each purpose: the commands, when to reach for them, the lesson where you used
them, and a short practice block that runs them on a fresh lab so you can see the output again.

## Lab setup

One small lab per section (the same scenarios as in the lessons):

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh ref-changes basic
bash scripts/new-lab.sh ref-branches diverged
bash scripts/new-lab.sh ref-remote remote
bash scripts/new-lab.sh ref-recovery history
bash scripts/new-lab.sh ref-advanced bisect
bash scripts/new-lab.sh ref-internals basic
```

## 1 · Repository

| Command | Use it when | Lesson |
|---|---|---|
| `git init [-b main]` | starting a new project | [06](../02-repositories/06-git-init/README.md) |
| `git clone URL [DIR]` | getting an existing project | [39](../09-remotes/39-git-clone/README.md) |
| `git clone --depth 1` / `--branch B` | fast CI clones / a specific branch | [39](../09-remotes/39-git-clone/README.md) |
| `git config --global user.name/email` | once per computer | [04](../01-fundamentals/04-first-configuration/README.md) |
| `git config --list --show-origin` | "where does this setting come from?" | [04](../01-fundamentals/04-first-configuration/README.md) |

Practise:

<!-- test: contains=Initialized empty Git repository; output -->
```bash
mkdir -p ~/git-practice/ref-repo && cd ~/git-practice/ref-repo
git init -b main
git config --show-origin --get user.name || echo "user.name not configured yet (lesson 04)"
```

```text
Initialized empty Git repository in ~/git-practice/ref-repo/.git/
file:~/.gitconfig	Ada Lovelace
```

## 2 · Changes

| Command | Use it when | Lesson |
|---|---|---|
| `git status [--short]` | always: before and after everything | [08](../02-repositories/08-git-status/README.md) |
| `git add FILE` / `git add -p` | choosing what goes into the next commit | [09](../03-commits/09-git-add/README.md), [10](../03-commits/10-staging-area/README.md) |
| `git diff` / `git diff --cached` | unstaged / staged changes | [15](../04-history/15-git-diff/README.md) |
| `git restore FILE` | throwing away unstaged edits (permanent) | [29](../07-undoing/29-restore-working-directory/README.md) |
| `git restore --staged FILE` | unstaging (safe) | [30](../07-undoing/30-unstage-files/README.md) |
| `git rm [--cached] FILE` / `git mv` | deleting / untracking / renaming | [73](../14-advanced-git/73-gitignore/README.md) |

Practise:

<!-- test: contains=M  menu.txt; contains= M prices.txt; output -->
```bash
cd ~/git-practice/ref-changes
echo "chai" >> menu.txt && sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add menu.txt
git status --short
git diff --cached --stat
```

```text
M  menu.txt
 M prices.txt
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

## 3 · Commits

| Command | Use it when | Lesson |
|---|---|---|
| `git commit -m "type(scope): message"` | recording a snapshot | [11](../03-commits/11-git-commit/README.md), [84](../17-hooks/84-commit-msg-hook/README.md) |
| `git commit --amend` | fixing the last (unpushed) commit | [12](../03-commits/12-inside-a-commit/README.md) |
| `git log --oneline --graph --all` | seeing the history | [13](../04-history/13-git-log/README.md), [16](../04-history/16-history-visualization/README.md) |
| `git log -S TEXT` / `-L 2,2:FILE` / `--author` | finding when something changed | [13](../04-history/13-git-log/README.md), [71](../14-advanced-git/71-git-blame/README.md) |
| `git show COMMIT[:FILE]` | one commit / a file at a commit | [14](../04-history/14-git-show/README.md) |
| `git blame -L FILE` | why is this line like this? | [71](../14-advanced-git/71-git-blame/README.md) |

Practise:

<!-- test: contains=feat(menu): add chai; output -->
```bash
cd ~/git-practice/ref-changes
git commit -q -m "feat(menu): add chai"
git log --oneline --graph -3
git show --stat --format='%h %an %s' HEAD
```

```text
* e82f06e (HEAD -> main) feat(menu): add chai
* 4267004 Add prices
* fc345e6 Add the menu
e82f06e Ada Lovelace feat(menu): add chai

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

## 4 · Branches

| Command | Use it when | Lesson |
|---|---|---|
| `git switch -c NAME` / `git switch NAME` | starting / changing tasks | [18](../05-branches/18-creating-branches/README.md)–[20](../05-branches/20-create-and-switch/README.md) |
| `git branch [-vv] [-d/-D NAME]` | listing / deleting | [21](../05-branches/21-branch-visualization/README.md), [22](../05-branches/22-deleting-branches/README.md) |
| `git merge [--no-ff/--ff-only] BRANCH` | integrating a branch | [23](../06-merging/23-what-is-merge/README.md)–[28](../06-merging/28-abort-merge/README.md) |
| `git rebase main` / `git rebase -i BASE` | updating / cleaning your own branch | [60](../13-rebase/60-what-is-rebase/README.md)–[66](../13-rebase/66-continue-rebase/README.md) |
| `git merge --abort` / `git rebase --abort` | backing out | [28](../06-merging/28-abort-merge/README.md), [65](../13-rebase/65-abort-rebase/README.md) |

Practise:

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
cd ~/git-practice/ref-branches
git branch -vv
git merge -q --no-edit feature-tea
git log --oneline --graph -4
```

```text
  feature-tea bb67674 Add green tea to the menu
* main        f40d080 Add opening hours
*   f5d438e (HEAD -> main) Merge branch 'feature-tea'
|\  
| * bb67674 (feature-tea) Add green tea to the menu
* | f40d080 Add opening hours
|/  
* 4267004 Add prices
```

## 5 · Remote

| Command | Use it when | Lesson |
|---|---|---|
| `git remote -v` / `add` / `set-url` | checking / connecting / changing the server | [37](../09-remotes/37-what-is-remote/README.md), [38](../09-remotes/38-git-remote/README.md) |
| `git fetch [--prune]` | seeing what changed, safely | [40](../09-remotes/40-git-fetch/README.md) |
| `git pull [--rebase / --ff-only]` | updating your branch | [41](../09-remotes/41-git-pull/README.md) |
| `git push [-u origin BRANCH]` | publishing | [42](../09-remotes/42-git-push/README.md), [43](../09-remotes/43-upstream-branches/README.md) |
| `git push --force-with-lease` | replacing your own rewritten branch | [42](../09-remotes/42-git-push/README.md) |
| `gh pr create / review / merge` | pull requests | [52](../11-pull-requests/52-create-pull-request/README.md)–[54](../11-pull-requests/54-merge-strategies/README.md) |

Practise:

<!-- test: contains=behind 'origin/main' by 1 commit; output -->
```bash
cd ~/git-practice/ref-remote
(cd grace && echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q)
cd ada && git fetch -q && git status | sed -n 2p
git log --oneline main..origin/main
```

```text
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
17bfab9 (origin/main, origin/HEAD) Add chai
```

## 6 · Recovery

| Command | Use it when | Lesson |
|---|---|---|
| `git reset --soft/--mixed/--hard REV` | moving your branch back (local commits) | [31](../07-undoing/31-git-reset/README.md) |
| `git revert COMMIT` / `-m 1 MERGE` | undoing pushed commits safely | [32](../07-undoing/32-git-revert/README.md) |
| `git reflog` / `ORIG_HEAD` | finding where you were | [33](../07-undoing/33-git-reflog/README.md), [79](../16-recovery/79-recover-deleted-branch/README.md)–[81](../16-recovery/81-recover-after-hard-reset/README.md) |
| `git fsck --lost-found` / `--unreachable` | last resort: dangling commits and blobs | [79](../16-recovery/79-recover-deleted-branch/README.md), [81](../16-recovery/81-recover-after-hard-reset/README.md) |
| `git branch NAME SHA` | rescuing a found commit | [79](../16-recovery/79-recover-deleted-branch/README.md) |

Practise:

<!-- test: contains=Price mocha; output -->
```bash
cd ~/git-practice/ref-recovery
git reset -q --hard HEAD~2
git reflog -2
git reset -q --hard ORIG_HEAD && git log --oneline -1
```

```text
269869e (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
ecff18a HEAD@{1}: commit: Price mocha
ecff18a (HEAD -> main) Price mocha
```

## 7 · Advanced

| Command | Use it when | Lesson |
|---|---|---|
| `git stash [push -m / pop / apply / list]` | parking unfinished work | [34](../08-stash/34-what-is-stash/README.md)–[36](../08-stash/36-managing-stashes/README.md) |
| `git cherry-pick [-x] COMMIT` | copying one commit (backports) | [67](../14-advanced-git/67-cherry-pick/README.md) |
| `git tag [-a/-s] vX.Y.Z` / `git describe` | releases | [68](../14-advanced-git/68-git-tags/README.md), [69](../14-advanced-git/69-annotated-tags/README.md) |
| `git bisect start / good / bad / run` | finding the commit that broke something | [70](../14-advanced-git/70-git-bisect/README.md) |
| `git clean -n / -fd` | removing untracked files (preview first) | [72](../14-advanced-git/72-git-clean/README.md) |
| `git worktree add / list / remove` | two branches checked out at once | [87](../18-advanced-repositories/87-git-worktrees/README.md) |
| `git submodule add / update --init` | embedding another repository | [86](../18-advanced-repositories/86-git-submodules/README.md) |
| `git lfs track` / `git lfs migrate` | large binary files | [88](../18-advanced-repositories/88-git-lfs/README.md) |

Practise:

<!-- test: contains=first bad commit: ; contains=Add mocha; output -->
```bash
cd ~/git-practice/ref-advanced
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh > /dev/null 2>&1
git log -1 --format='first bad commit: %h %s' refs/bisect/bad
git bisect reset > /dev/null 2>&1
git stash list | wc -l
```

```text
first bad commit: 3ceea03 Add mocha
0
```

## 8 · Inside Git and security

| Command | Use it when | Lesson |
|---|---|---|
| `git cat-file -t/-p OBJECT` | looking at blobs, trees, commits | [74](../15-git-internals/74-how-git-stores-data/README.md), [75](../15-git-internals/75-git-objects/README.md) |
| `git rev-parse REV` / `git symbolic-ref HEAD` | resolving names, HEAD | [76](../15-git-internals/76-head/README.md), [77](../15-git-internals/77-branches-are-references/README.md) |
| `git hook run NAME`, `core.hooksPath` | testing and sharing hooks | [82](../17-hooks/82-what-are-hooks/README.md)–[85](../17-hooks/85-hooks-in-teams/README.md) |
| `git log -S SECRET --all`, `git filter-repo` | finding and removing leaked data | [89](../19-security/89-secrets-in-git/README.md), [90](../19-security/90-removing-sensitive-data/README.md) |
| `git commit -S`, `git verify-commit`, `gpg.format ssh` | signed commits and tags | [91](../19-security/91-commit-signing/README.md) |

Practise:

<!-- test: contains=commit; contains=tree; output -->
```bash
cd ~/git-practice/ref-internals
git cat-file -t HEAD
git cat-file -p HEAD | head -2
git symbolic-ref HEAD
```

```text
commit
tree edd9d5aca7be17de9c83a80dc687991f6f56e24d
parent fc345e6b28df7fdfd7f872b37d78b47d0d024103
refs/heads/main
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/ref-repo ~/git-practice/ref-changes ~/git-practice/ref-branches ~/git-practice/ref-remote ~/git-practice/ref-recovery ~/git-practice/ref-advanced ~/git-practice/ref-internals
```

When a situation goes wrong rather than a command: [Module 22 · Troubleshooting](../22-troubleshooting/README.md).
