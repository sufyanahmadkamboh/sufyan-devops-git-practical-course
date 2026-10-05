<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 06 · git init · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Run `git init` a second time in `git-demo` after making a commit. Prove that the commit survives.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-06/git-demo
git add README.md && git commit -q -m "First commit"
git init
git log --oneline
```

```text
Reinitialized existing Git repository in ~/git-practice/lesson-06/git-demo/.git/
e750ab0 First commit
```

`Reinitialized existing Git repository`: `git init` never deletes history.

</details>
