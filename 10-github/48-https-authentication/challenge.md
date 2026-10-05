<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 48 · HTTPS authentication · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Which scopes does your current `gh` token have, and which one allows pushing to repositories?

<details>
<summary>Solution</summary>

```bash
gh auth status --active 2>&1 | grep -i scopes
```

```text
  - Token scopes: 'gist', 'read:org', 'repo', 'user', 'workflow'
```

`repo` gives full access to your repositories (pushing included); `workflow` is additionally needed to push changes
to `.github/workflows/` files.

</details>
