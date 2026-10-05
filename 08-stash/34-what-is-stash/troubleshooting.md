<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 34 · What is a stash? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Stash when your work includes a **new** file:

```bash
echo "Monday: free cookie" > specials.txt
git stash
git status --short
```

```text
Saved working directory and index state WIP on main: 8c1f1e8 Fix the espresso price
?? specials.txt
```

## Troubleshoot

The modified tracked files were stashed, but `specials.txt` is still there: by default `git stash` ignores
**untracked** files. If you now switch branches or reset, the new file travels with you or gets in the way.

## Fix

Pop the stash, then stash again with `-u` (include untracked):

```bash
git stash pop -q
git stash -u
git status
git stash pop -q
```

```text
Saved working directory and index state WIP on main: 8c1f1e8 Fix the espresso price
On branch main
nothing to commit, working tree clean
```
