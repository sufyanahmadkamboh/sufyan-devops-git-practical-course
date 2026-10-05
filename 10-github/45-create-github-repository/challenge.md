<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 45 · Creating a GitHub repository · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Add topics to the repository from the command line (`gh repo edit`), then show them.

<details>
<summary>Solution</summary>

```bash
me=$(gh api user --jq .login)
gh repo edit "$me/git-practice-cafe" --add-topic git --add-topic practice > /dev/null
gh repo view git-practice-cafe --json repositoryTopics --jq '[.repositoryTopics[].name] | join(", ")'
```

```text
git, practice
```

</details>
