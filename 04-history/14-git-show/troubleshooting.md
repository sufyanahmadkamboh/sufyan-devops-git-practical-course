<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 14 · git show · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

```bash
git show HEAD~4:hours.txt 2>&1
```

```text
fatal: path 'hours.txt' does not exist in 'HEAD~4'
```

## Troubleshoot

`path 'hours.txt' does not exist in 'HEAD~4'`: the file did not exist in that commit (or the path is wrong). List what
was in that snapshot:

```bash
git show --name-only --format= HEAD~4
git ls-tree --name-only HEAD~4
```

## Fix

Ask for a file that existed in that commit:

```bash
git show HEAD~4:menu.txt
```
