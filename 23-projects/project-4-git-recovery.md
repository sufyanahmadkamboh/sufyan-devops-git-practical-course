# Project 4 · Git recovery

> Level 24 · Projects · advanced · ⏱ 60 minutes · lessons 31–36, 78–81

## Brief

A colleague had a very bad afternoon in the shared cafe repository's clone and asks you to save what can be saved.
The script below replays the afternoon. Recover **all four** pieces of lost work, without asking Git to forget
anything else.

| Lost work | How it was lost |
|---|---|
| the "seasonal menu" branch (2 commits) | `git branch -D` |
| the commit "Price the flat white" | `git reset --hard HEAD~1` |
| a hotfix commit made while checking an old tag | committed in detached HEAD, then switched away |
| the stash "WIP: tea descriptions" | `git stash drop` |

## Requirements

1. Branch `seasonal-menu` exists again with both of its commits.
2. `main` contains "Price the flat white" again.
3. Branch `hotfix-espresso` points to the detached-HEAD hotfix commit.
4. The stash's changes are back, as a stash entry or as a branch `wip-tea`.
5. Nothing that existed before the afternoon is lost.

## Starting point

<!-- test: contains=afternoon replayed -->
```bash
bash scripts/new-lab.sh project-4 basic
cd ~/git-practice/project-4
git switch -q -c seasonal-menu
echo "pumpkin latte" >> menu.txt && git commit -q -am "Add pumpkin latte"
echo "pumpkin latte 4.20" >> prices.txt && git commit -q -am "Price pumpkin latte"
git switch -q main && git branch -q -D seasonal-menu
echo "flat white" >> menu.txt && git commit -q -am "Add flat white"
echo "flat white 3.60" >> prices.txt && git commit -q -am "Price the flat white"
git reset -q --hard HEAD~1
git tag v1.0.0 4267004 && git switch -q --detach v1.0.0
sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix: espresso price"
git switch -q main 2> /dev/null
sed -i 's/^latte$/latte (with oat milk)/' menu.txt && git stash push -q -m "WIP: tea descriptions"
git stash drop -q
git log --oneline --all
echo "afternoon replayed"
```

## Hints

- Committed work: `git reflog` (lessons 33, 79–81). Deleted stashes: `git fsck --unreachable` (lesson 36).
- Mark every find with a branch before doing anything else (`git branch NAME SHA`).

## Reference solution

<details>
<summary>Show the reference solution</summary>

<!-- test: contains=Price pumpkin latte; contains=Price the flat white; contains=Hotfix; output -->
```bash
cd ~/git-practice/project-4
git reflog --format='%h %gs' | grep -E "commit: (Price pumpkin|Price the flat|Hotfix)"
```

```text
6c51618 commit: Hotfix: espresso price
7f6144c commit: Price the flat white
673da75 commit: Price pumpkin latte
```

<!-- test: contains=recovered; output -->
```bash
find() { git reflog --format=%h --grep-reflog="commit: $1" | head -1; }
git branch seasonal-menu "$(find 'Price pumpkin latte')"
git merge -q --ff-only "$(find 'Price the flat white')"
git branch hotfix-espresso "$(find 'Hotfix: espresso price')"
stash=$(for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/WIP: tea descriptions/ {print $1}')
git branch wip-tea "$stash"
echo "recovered: seasonal-menu, flat white price, hotfix-espresso, wip-tea"
```

```text
recovered: seasonal-menu, flat white price, hotfix-espresso, wip-tea
```

</details>

## Self-check

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-4
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "seasonal-menu with both commits"     '[ "$(git rev-list --count main..seasonal-menu)" -ge 2 ] || git log --oneline seasonal-menu | grep -q "Add pumpkin latte"'
check "main has the flat white price"       'git show main:prices.txt | grep -q "flat white 3.60"'
check "hotfix-espresso has the hotfix"      'git show hotfix-espresso:prices.txt | grep -q "espresso 2.45"'
check "the stashed change is recoverable"   'git stash list | grep -q "tea descriptions" || git show wip-tea:menu.txt | grep -q "oat milk"'
check "nothing else lost (Add prices)"      'git merge-base --is-ancestor 4267004 main'
```

```text
ok       seasonal-menu with both commits
ok       main has the flat white price
ok       hotfix-espresso has the hotfix
ok       the stashed change is recoverable
ok       nothing else lost (Add prices)
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/project-4
```

Next: [Project 5 · Release management](project-5-release-management.md)
