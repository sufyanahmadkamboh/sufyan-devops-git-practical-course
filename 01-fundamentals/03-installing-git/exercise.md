<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 03 · Installing Git · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Find out where your Git installation keeps its *system-wide* configuration file.

**Expected result.** A file path (for example `/etc/gitconfig` on Linux), or an empty answer if Git was built without
one.

**Verification.**

<!-- test -->
```bash
git config --system --list --show-origin 2>/dev/null | head -3 || true
git version --build-options | head -3
```
