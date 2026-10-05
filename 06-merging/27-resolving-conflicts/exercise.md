<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 27 · Resolving merge conflicts · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Recreate the conflict (a fresh lab) and resolve it by keeping **their** version (`feature-tea`'s
3.50) for the whole file, without typing the content.

**Expected result.** `latte 3.50`, a merge commit.

**Verification.**

```bash
cd ~/git-practice/lesson-27
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git checkout --theirs prices.txt && git add prices.txt && git commit -q --no-edit
grep latte prices.txt
```
