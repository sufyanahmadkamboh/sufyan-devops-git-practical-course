<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 39 · git clone · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Clone into a folder that already has files:

```bash
cd ~/git-practice/lesson-39
git clone server/cafe.git ada 2>&1
```

```text
fatal: destination path 'ada' already exists and is not an empty directory.
```

## Troubleshoot

`destination path 'ada' already exists and is not an empty directory.`: Git never clones over existing files. Either
the repository is already there (then you need `git pull` inside it, not a new clone), or choose another folder.

```bash
git -C ada remote -v
```

## Fix

```bash
git clone -q server/cafe.git ada-2
ls
```
