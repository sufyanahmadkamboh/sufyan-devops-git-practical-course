<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 59 · Branch protection · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

List which of your practice repository's branches are protected.

<details>
<summary>Solution</summary>

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches?protected=true" --jq '.[].name'
```

```text
main
```

</details>
