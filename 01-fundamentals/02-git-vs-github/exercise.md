<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 02 · Git vs GitHub · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Make a new commit in `~/git-practice/lesson-02` (any change), then push it to the bare repository.

**Expected result.** The bare "server" has the same latest commit as your local `main`.

**Verification.**

```bash
cd ~/git-practice/lesson-02
git log --oneline -1
git --git-dir ~/git-practice/lesson-02-server/cafe.git log --oneline -1
```
