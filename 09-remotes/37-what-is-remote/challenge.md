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
958330b4325970f21538eb43bc187658891a6c0c	refs/heads/main
958330b4325970f21538eb43bc187658891a6c0c
```

`git ls-remote` asks the server directly without updating anything locally.

</details>
