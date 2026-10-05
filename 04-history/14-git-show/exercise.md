<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 14 · git show · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show who wrote the commit that added green tea's price, and when, without its diff.

**Expected result.** One line with author and date.

**Verification.**

```bash
cd ~/git-practice/lesson-14
git show -s --format='%h %an %ad %s' "$(git log --format=%h --grep='Price green tea')"
```
