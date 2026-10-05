<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 26 · Merge conflicts · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Ignore the conflict and try to commit:

```bash
git commit -m "Merge" 2>&1
```

```text
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U	prices.txt
```

## Troubleshoot

`Committing is not possible because you have unmerged files.`: Git will not record a merge while a file is still in
conflict. `git status` explains where you are:

```bash
git status
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

## Fix

Resolution is lesson 27. For now, step back out of the merge (lesson 28):

```bash
git merge --abort
git status
```
