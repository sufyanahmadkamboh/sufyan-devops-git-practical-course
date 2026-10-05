<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 56 · Feature branch workflow · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the remote feature branches and how far each is behind `origin/main`.

**Expected result.** `feature/menu-tea` 0 behind (it was just updated).

**Verification.**

```bash
cd ~/git-practice/lesson-56/ada
git push -q
for b in $(git branch -r --format='%(refname:short)' | grep feature/); do echo "$b $(git rev-list --count "$b..origin/main") behind"; done
```
