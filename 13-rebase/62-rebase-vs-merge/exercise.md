<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 62 · Rebase vs merge · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show only the merge commits of each branch.

**Expected result.** One on `merge-way`, none on `rebase-way`.

**Verification.**

```bash
cd ~/git-practice/lesson-62
for b in merge-way rebase-way; do echo "$b: $(git rev-list --merges --count "$b")"; done
```
