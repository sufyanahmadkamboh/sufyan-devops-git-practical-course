<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 80 · Recover a deleted commit · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** An `--amend` replaced a commit's content. Make one, then show the commit **before** the amend.

**Expected result.** The reflog's `commit (amend)` line, and the previous version's message.

**Verification.**

```bash
cd ~/git-practice/lesson-80
git reflog -2
git log -1 --format=%s 'HEAD@{1}'
```
