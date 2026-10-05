<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 71 · Git blame · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show the complete history of the latte line, not only the last change.

**Expected result.** Two commits: "Raise the latte price to 3.30" and "Add prices".

**Verification.**

```bash
cd ~/git-practice/lesson-71
git log --oneline -L 2,2:prices.txt | grep -E "^[0-9a-f]{7} "
```
