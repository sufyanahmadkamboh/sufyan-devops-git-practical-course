<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 97 · Releases · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Download v1.0.0's asset into a new folder and check its contents.

**Expected result.** `menu.txt` and `prices.txt` with the 1.0.0 prices.

**Verification.**

```bash
cd ~/git-practice/lesson-97
mkdir -p ../lesson-97-download && gh release download v1.0.0 -D ../lesson-97-download --clobber
tar -xzf ../lesson-97-download/menu-v1.0.0.tar.gz -O prices.txt
```
