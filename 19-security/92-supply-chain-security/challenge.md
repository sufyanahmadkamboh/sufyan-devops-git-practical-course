<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 92 · Supply chain security · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Resolve the current commit ID behind a public tag, as you would before pinning an action.

<details>
<summary>Solution</summary>

```bash
git ls-remote https://github.com/actions/checkout refs/tags/v4 'refs/tags/v4^{}'
```

```text
11d5960a326750d5838078e36cf38b85af677262	refs/tags/v4
```

For an annotated tag, the `^{}` line is the commit it points to: pin that 40-character ID, with the tag name as a
comment (`uses: actions/checkout@<sha> # v4`).

</details>
