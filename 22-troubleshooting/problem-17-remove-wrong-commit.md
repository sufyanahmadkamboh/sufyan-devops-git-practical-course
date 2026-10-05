# Problem 17 · Wrong commit needs to be removed

> Troubleshooting lab · run every command from the course folder · related lessons: [31](../07-undoing/31-git-reset/README.md), [32](../07-undoing/32-git-revert/README.md), [63](../13-rebase/63-interactive-rebase/README.md)

## Problem

A wrong commit sits in the **middle** of the history: "Debug: log all orders", which writes customer data to a log.
It must go, but the commits after it must stay.

<!-- test: contains=lesson-t17 -->
```bash
bash scripts/new-lab.sh lesson-t17 remote
cd ~/git-practice/lesson-t17/ada
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
echo "log_orders=true" > debug.conf && git add debug.conf && git commit -q -m "Debug: log all orders"
echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push -q
```

## Symptoms

`debug.conf` is in `main`; removing the latest commit would also remove "Add mocha".

<!-- test: contains=Debug: log all orders; output -->
```bash
git log --oneline -4
```

```text
32c5d4c (HEAD -> main, origin/main, origin/HEAD) Add mocha
45992be Debug: log all orders
3301201 Add green tea
4267004 Add prices
```

## Investigation

Is it pushed? What exactly does it change? Does anything later depend on it?

<!-- test: contains=debug.conf; output -->
```bash
git branch -r --contains "$(git log --format=%h -1 --grep='^Debug')"
git show --stat --format=%s "$(git log --format=%h -1 --grep='^Debug')"
git log --oneline "$(git log --format=%h -1 --grep='^Debug')"..main -- debug.conf | wc -l
```

```text
  origin/HEAD -> origin/main
  origin/main
Debug: log all orders

 debug.conf | 1 +
 1 file changed, 1 insertion(+)
0
```

## Commands

| Command | Shows |
|---|---|
| `git branch -r --contains SHA` | whether the commit is on the server |
| `git show --stat SHA` | what it changes |
| `git log SHA..main -- FILE` | later commits touching the same file (0 = independent) |

## Understand the output

It is on `origin/main` (pushed), it only adds `debug.conf`, and no later commit touches that file: it can be undone
on its own.

## Root cause

A debugging change was committed together with real work and pushed without review.

## Fix

Choose by whether the commit is shared:

- **Pushed / shared** (this case): `git revert` it: a new commit that removes exactly its change, safe for everyone.
- **Only local**: drop it with `git rebase -i` (lesson 63), so it never existed.

<!-- test: contains=Revert "Debug: log all orders"; output -->
```bash
git revert --no-edit "$(git log --format=%h -1 --grep='^Debug')" 2>&1 | head -1
git push -q
git log --oneline -4
```

```text
[main 0a80f2d] Revert "Debug: log all orders"
0a80f2d (HEAD -> main, origin/main, origin/HEAD) Revert "Debug: log all orders"
32c5d4c Add mocha
45992be Debug: log all orders
3301201 Add green tea
```

If the commit had contained a **secret** or personal data that must not remain in history at all, revert is not
enough: follow Problem 12 (rotate, rewrite with `git filter-repo`, force-push, re-clone).

## Verification

<!-- test: contains=mocha; output -->
```bash
ls debug.conf 2>&1 | sed 's/.*No such file.*/debug.conf: gone/'
tail -1 menu.txt
```

```text
debug.conf: gone
mocha
```

## Prevention

- Review `git diff --cached` before committing; keep debugging changes on a separate branch or in `.gitignore`d files.
- Pull requests with review before anything reaches `main`.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t17
```

Next: [Problem 18 · Production branch contains an unwanted commit](problem-18-unwanted-commit-production.md)
