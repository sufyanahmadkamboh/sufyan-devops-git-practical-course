<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 37 · What is a remote? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without fetching, find out what the server's `main` points to **right now**, and compare it with Ada's `origin/main`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-37/ada
git ls-remote origin main
git rev-parse origin/main
```

```text
ee8ab62f3196c5eabc42d26afcb7e7000db73ab8	refs/heads/main
ee8ab62f3196c5eabc42d26afcb7e7000db73ab8
```

`git ls-remote` asks the server directly without updating anything locally.

</details>
