<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 01 · What is Git? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Delete the file, as if by accident:

```bash
cd ~/git-practice/lesson-01/with-git
rm prices.txt
ls; git status --short; echo "(prices.txt deleted)"
```

## Troubleshoot

`git status` (lesson 08) shows ` D prices.txt`: Git noticed the file is gone. In the no-Git folder, a deleted file is
simply gone. Here, every committed version still exists inside the repository.

## Fix

```bash
git restore prices.txt
cat prices.txt
```

```text
espresso 2.50
latte 3.30
cappuccino 3.40
mocha 3.90
```
