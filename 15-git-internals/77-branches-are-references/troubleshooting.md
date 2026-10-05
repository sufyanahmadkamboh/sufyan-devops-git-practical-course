<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 77 · Branches are references · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Delete a branch reference and look for "its" commits:

```bash
git update-ref -d refs/heads/feature-tea
git branch
git log --oneline --all | head -3
```

```text
  experiment
* main
4267004 (HEAD -> main, experiment) Add prices
fc345e6 Add the menu
d6df412 Add README
```

## Troubleshoot

The commit "Add green tea to the menu" no longer appears in `git log --all`: nothing references it. It still exists:
deleting a branch deleted a pointer, not commits.

```bash
git cat-file -p bb67674 | tail -1
```

```text
Add green tea to the menu
```

## Fix

Recreate the reference to the same commit (the ID was in the earlier output, or in `git reflog`):

```bash
git branch feature-tea bb67674
git log --oneline -1 feature-tea
```

```text
bb67674 (feature-tea) Add green tea to the menu
```
