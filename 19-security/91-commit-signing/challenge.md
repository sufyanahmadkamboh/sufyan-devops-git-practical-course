<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 91 · Commit signing · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create a **signed annotated tag** for the release and verify it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-91
git tag -s v1.0.0 -m "Release 1.0.0"
git verify-tag v1.0.0 2>&1 | sed "s|$HOME|~|"
```

```text
Good "git" signature for ada@example.com with ED25519 key SHA256:26wG0fLnNNF6vVyYVwEA66m+t7NSNSijllSiFb0Wmic
```

</details>
