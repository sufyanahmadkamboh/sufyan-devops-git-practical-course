<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 19 · Switching branches · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Now an uncommitted change to a file that **differs** between the branches:

```bash
git restore prices.txt
echo "matcha" >> menu.txt
git switch main 2>&1
```

```text
error: Your local changes to the following files would be overwritten by checkout:
	menu.txt
Please commit your changes or stash them before you switch branches.
Aborting
```

## Troubleshoot

`Your local changes to the following files would be overwritten by checkout: menu.txt`. `menu.txt` is different on
`main`; switching would have to replace your edited version, so Git refuses rather than destroy your work. You are still
on `feature-tea`, nothing was lost:

```bash
git branch --show-current
git status --short
```

## Fix

Three options: commit the change, stash it (lesson 35), or discard it. Commit it here:

```bash
git commit -q -am "Add matcha"
git switch main
git branch --show-current
```
