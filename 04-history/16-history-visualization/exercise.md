<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 16 · Commit history visualization · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show only the main line of history, the way a release manager sees it: merges, not the commits that
came from branches.

**Expected result.** The merge commit appears, `Add green tea` does not.

**Verification.**

```bash
cd ~/git-practice/lesson-16
git log --oneline --first-parent
```
