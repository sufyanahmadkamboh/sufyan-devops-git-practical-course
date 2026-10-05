<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 97 · Releases · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Which release does GitHub mark as **Latest**, and why not v1.1.0 even though it was edited last?

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-97
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/releases/latest" --jq .tag_name
```

```text
v2.0.0
```

"Latest" is the highest semantic version among non-prerelease releases by default, not the most recently edited.

</details>
