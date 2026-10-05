<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 61 · Basic rebase · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Rebase with uncommitted changes in your folder:

```bash
git switch -q main && git switch -q -c feature-mocha HEAD~3
echo "mocha" > specials.txt && git add specials.txt && git commit -q -m "Add mocha special"
sed -i 's/espresso 2.50/espresso 2.55/' prices.txt
git rebase main 2>&1
```

```text
error: cannot rebase: You have unstaged changes.
error: Please commit or stash them.
```

## Troubleshoot

`cannot rebase: You have unstaged changes.`: rebase rewrites the working directory commit by commit; it refuses to
risk your uncommitted work. `git status` shows the draft change in `prices.txt`.

## Fix

Let Git stash and restore it around the rebase:

```bash
git rebase --autostash main 2>&1 | grep -v "^hint:" || true
git status --short
```

```text
Created autostash: 8928ff6
Rebasing (1/1)
Applied autostash.
Successfully rebased and updated refs/heads/feature-mocha.
 M prices.txt
```

The draft (`M prices.txt`) is back, on top of the rebased branch.
