<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 73 · .gitignore · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Ignore your editor's folder `.vscode/` only for yourself (not in the shared `.gitignore`).

**Expected result.** `git check-ignore -v` points to `.git/info/exclude`.

**Verification.**

```bash
cd ~/git-practice/lesson-73
git check-ignore -v .vscode/settings.json
```
