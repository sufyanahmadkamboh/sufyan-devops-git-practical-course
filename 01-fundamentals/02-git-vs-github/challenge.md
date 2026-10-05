<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 02 · Git vs GitHub · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without cloning it, find out which branch the public repository `https://github.com/git/git` uses as its default
(`HEAD`).

<details>
<summary>Solution</summary>

```bash
git ls-remote --symref https://github.com/git/git HEAD
```

```text
ref: refs/heads/master	HEAD
8103b446517e0c44e67561b9d0ccce56efa60a71	HEAD
```

`--symref` shows what the remote's `HEAD` points to: its default branch.

</details>
