<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 05 · What is a Git repository? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** From a subfolder of the lab, ask Git where the repository is.

**Expected result.** Git finds `.git` in the parent folder: commands work from anywhere inside the project.

**Verification.**

```bash
cd ~/git-practice/lesson-05
mkdir -p docs/notes && cd docs/notes
git rev-parse --show-toplevel --git-dir
```
