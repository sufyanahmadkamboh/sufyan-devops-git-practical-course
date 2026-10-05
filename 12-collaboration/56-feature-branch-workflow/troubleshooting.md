<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 56 · Feature branch workflow · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A long-lived branch: Grace starts `feature/new-prices`, works on it for "three weeks" without updating, while `main`
keeps changing the same file:

```bash
cd ~/git-practice/lesson-56/grace && git pull -q
git switch -q -c feature/new-prices
sed -i 's/espresso 2.50/espresso 2.70/; s/cappuccino 3.40/cappuccino 3.60/' prices.txt && git commit -q -am "New prices"
cd ../ada && git switch -q main && git merge -q feature/menu-tea && git pull -q --no-rebase --no-edit
for p in 2.55 2.60 2.65; do sed -i "s/^espresso .*/espresso $p/" prices.txt && git commit -q -am "Espresso $p" && git push -q; done
cd ../grace && git fetch -q && git merge origin/main 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

## Troubleshoot

Three weeks of `main` against three weeks of branch: the longer they diverge, the more overlapping changes, the
harder the conflict, and the less anyone remembers why each change was made.

```bash
git rev-list --left-right --count HEAD...origin/main | awk '{print "branch has", $1, "own commit(s); main has", $2, "new commit(s)"}'
git merge --abort
```

```text
branch has 1 own commit(s); main has 5 new commit(s)
```

## Fix

Resolve once (keep the new prices for both items), then keep the branch fresh: merge `main` in every day, or after
every merged PR that touches the same area.

```bash
git merge origin/main > /dev/null 2>&1 || true
git checkout --ours prices.txt && git add prices.txt && git commit -q --no-edit
head -1 prices.txt
```

```text
Updated 1 path from the index
espresso 2.70
```
