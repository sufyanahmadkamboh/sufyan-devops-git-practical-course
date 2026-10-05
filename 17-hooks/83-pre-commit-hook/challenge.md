<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 83 · Pre-commit hook · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Test the hook without committing: stage a 2 MB file and run the hook directly.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-83
head -c 2097152 /dev/zero > big.bin && git add big.bin
git hook run pre-commit 2>&1 || true
git restore --staged big.bin && rm big.bin
```

```text
pre-commit: big.bin is larger than 1 MB (use Git LFS, lesson 88)
commit blocked: fix the files above (or unstage them)
```

</details>
