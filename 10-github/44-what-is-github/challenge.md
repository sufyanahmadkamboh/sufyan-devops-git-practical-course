<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 44 · What is GitHub? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Using `gh`, show the description and default branch of `octocat/Hello-World`.

<details>
<summary>Solution</summary>

```bash
gh repo view octocat/Hello-World --json description,defaultBranchRef --jq '.description, .defaultBranchRef.name'
```

```text
My first repository on GitHub!
master
```

`gh` is GitHub's own command-line tool (install: <https://cli.github.com>); it talks to GitHub's API, not just to Git.

</details>
