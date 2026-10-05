<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 05 · What is a Git repository? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without `git log`, find the commit message of the latest commit by following `HEAD` yourself with
`git cat-file -p`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-05
ref=$(sed 's/ref: //' .git/HEAD)
id=$(cat ".git/$ref")
git cat-file -p "$id"
```

```text
tree edd9d5aca7be17de9c83a80dc687991f6f56e24d
parent fc345e6b28df7fdfd7f872b37d78b47d0d024103
author Ada Lovelace <ada@example.com> 1767603780 +0000
committer Ada Lovelace <ada@example.com> 1767603780 +0000

Add prices
```

`HEAD` → `refs/heads/main` → a commit ID → the commit object, with its tree, parent, author and message. Lesson 75
explores objects in depth.

</details>
