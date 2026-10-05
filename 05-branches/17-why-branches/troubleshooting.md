<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 17 · Why branches exist · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Back in the single-branch lab: the release manager wants to ship the latte fix without the loyalty work. On one
branch, the two are in a line; you cannot take one without the other.

```bash
cd ~/git-practice/lesson-17
git log --oneline main
```

## Troubleshoot

The history is linear: `Fix the latte price` sits on top of `WIP: loyalty card`. Releasing the commit with the fix
means releasing everything below it.

## Fix

Undo the mix-up the way a team would: move the unfinished work to its own branch, and rebuild `main` with only the fix
(lesson 67 explains `cherry-pick`; here it copies the fix):

```bash
cd ~/git-practice/lesson-17
fix=$(git rev-parse HEAD)                    # remember the fix commit (the latest one)
git branch feature-loyalty HEAD~1            # a branch that keeps the WIP commit
git reset -q --hard HEAD~2                   # main back to before the WIP (lesson 31)
git cherry-pick "$fix" > /dev/null           # copy only the fix onto main
git log --oneline main
```

```text
35f851e (HEAD -> main) Fix the latte price
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```
