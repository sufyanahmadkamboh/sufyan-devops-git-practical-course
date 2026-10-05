<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 20 · Create and switch in one command · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

The most common mistake: starting a new branch from the **wrong** branch. You are on `fix-tea-price` and start a new
feature from here without noticing:

```bash
git switch -q fix-tea-price
git switch -c feature-specials
echo "Monday special" > specials.txt && git add specials.txt && git commit -q -m "Add specials"
git log --oneline main..feature-specials
```

```text
Switched to a new branch 'feature-specials'
5d6c90c (HEAD -> feature-specials) Add specials
bb67674 (fix-tea-price, feature-tea) Add green tea to the menu
```

## Troubleshoot

`main..feature-specials` should show only "Add specials", but it also contains "Add green tea to the menu": the new
branch inherited everything from the branch it started on. Always check where you are (`git branch --show-current`)
before `git switch -c`, or name the start point explicitly.

## Fix

Rebuild the branch from `main` with only its own commit (lesson 61 explains `rebase --onto`):

```bash
git rebase -q --onto main fix-tea-price feature-specials
git log --oneline main..feature-specials
```

```text
3485fa5 (HEAD -> feature-specials) Add specials
```
