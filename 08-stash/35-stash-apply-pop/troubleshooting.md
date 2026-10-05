<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 35 · Stash, apply and pop · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Pop a stash onto a version of the file that changed since you stashed it, on the same lines:

```bash
git commit -q -am "Espresso 2.60"
sed -i 's/^green tea$/green tea (sencha)/' menu.txt && git commit -q -am "Sencha"
git stash pop 2>&1
```

```text
Auto-merging menu.txt
CONFLICT (content): Merge conflict in menu.txt
On branch feature-tea
Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   menu.txt

no changes added to commit (use "git add" and/or "git commit -a")
The stash entry is kept in case you need it again.
```

## Troubleshoot

The stash's `chai` line was added right after `green tea`, which was changed since: a conflict, resolved like a merge.
Note the last line: `The stash entry is kept in case you need it again.`

```bash
git status --short
git stash list
```

```text
UU menu.txt
stash@{0}: On feature-tea: chai
```

## Fix

Resolve (keep both lines), mark resolved, and drop the stash yourself since `pop` did not:

```bash
printf 'espresso\nlatte\ncappuccino\ngreen tea (sencha)\nchai\n' > menu.txt
git restore --staged menu.txt
git stash drop
cat menu.txt
```

```text
Dropped refs/stash@{0} (52f0ff2474b2a1d0724a47861a67dadf7e15559c)
espresso
latte
cappuccino
green tea (sencha)
chai
```

`git restore --staged` here only clears the "unmerged" state; the resolved file stays as uncommitted work, like after a
normal pop.
