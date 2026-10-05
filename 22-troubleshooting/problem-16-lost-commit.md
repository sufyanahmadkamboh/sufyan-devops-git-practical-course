# Problem 16 · Lost commit

> Troubleshooting lab · run every command from the course folder · related lessons: [33](../07-undoing/33-git-reflog/README.md), [80](../16-recovery/80-recover-deleted-commit/README.md), [64](../13-rebase/64-rebase-conflicts/README.md)

## Problem

During a `git pull --rebase` with a conflict, you ran `git rebase --skip` to "get past it". Later you notice your
commit is gone.

<!-- test: contains=lesson-t16 -->
```bash
bash scripts/new-lab.sh lesson-t16 remote
cd ~/git-practice/lesson-t16
(cd grace && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Latte 3.30" && git push -q)
cd ada
sed -i 's/latte 3.20/latte 3.50/' prices.txt && echo "chai 3.10" >> prices.txt && git commit -q -am "New latte price and chai"
git pull --rebase > /dev/null 2>&1 || git rebase --skip > /dev/null 2>&1
```

## Symptoms

<!-- test: contains=chai is missing; output -->
```bash
git log --oneline -3
grep chai prices.txt || echo "chai is missing"
```

```text
e87a5d6 (HEAD -> main, origin/main, origin/HEAD) Latte 3.30
4267004 Add prices
fc345e6 Add the menu
chai is missing
```

## Investigation

The commit was never pushed, so only this clone's reflog knows it:

<!-- test: contains=New latte price and chai; output -->
```bash
git reflog | grep -E "commit: |rebase" | head -5
```

```text
e87a5d6 (HEAD -> main, origin/main, origin/HEAD) HEAD@{0}: rebase (finish): returning to refs/heads/main
e87a5d6 (HEAD -> main, origin/main, origin/HEAD) HEAD@{1}: pull --rebase (start): checkout e87a5d6a9d8affc36bc27704785d20df9b593136
570542f HEAD@{2}: commit: New latte price and chai
```

## Commands

| Command | Shows |
|---|---|
| `git reflog` | every position of HEAD, including commits no branch contains |
| `git log -g --grep-reflog=TEXT` | search it |
| `git show SHA` | the lost commit's change |
| `git fsck --unreachable` | if the reflog does not have it (lesson 79) |

## Understand the output

`commit: New latte price and chai` is your commit; then `rebase (start)` and `rebase (finish)` without a `pick`
line for it: `--skip` dropped the whole commit, including the chai line that had nothing to do with the conflict.

## Root cause

`git rebase --skip` means "drop this commit", not "skip the conflict".

## Fix

Re-apply the lost commit; it conflicts again on the latte line, this time resolve it properly (keep chai, agree on the
latte price):

<!-- test: contains=chai 3.10; output -->
```bash
lost=$(git reflog --format=%h --grep-reflog="commit: New latte price and chai" | head -1)
git cherry-pick "$lost" > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.30\ncappuccino 3.40\nchai 3.10\n' > prices.txt
git add prices.txt && git -c core.editor=true cherry-pick --continue > /dev/null
cat prices.txt
```

```text
espresso 2.50
latte 3.30
cappuccino 3.40
chai 3.10
```

## Verification

<!-- test: contains=New latte price and chai; output -->
```bash
git log --oneline -3
git push 2>&1 | tail -1
```

```text
1062d2a (HEAD -> main) New latte price and chai
e87a5d6 (origin/main, origin/HEAD) Latte 3.30
4267004 Add prices
   e87a5d6..1062d2a  main -> main
```

## Prevention

- In a conflict, resolve or `--abort`; use `--skip` only when you want the commit gone.
- Small commits: a conflict in one change does not put unrelated changes at risk.
- Push work early; the server and teammates keep copies.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t16
```

Next: [Problem 17 · Wrong commit needs to be removed](problem-17-remove-wrong-commit.md)
