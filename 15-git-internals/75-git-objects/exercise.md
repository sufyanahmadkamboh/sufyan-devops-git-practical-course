<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 75 · Git objects · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show the index entry for `menu.txt` (mode, blob ID, stage).

**Expected result.** `100644 <blob> 0	menu.txt`, the same blob ID as in the tree.

**Verification.**

```bash
cd ~/git-practice/lesson-75
git ls-files --stage menu.txt
git rev-parse HEAD:menu.txt
```
