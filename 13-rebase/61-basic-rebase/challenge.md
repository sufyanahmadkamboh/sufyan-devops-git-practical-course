<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 61 · Basic rebase · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

From `main`, rebase `feature-mocha` onto `main` in one command, and list the commits it has that `main` does not.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-61
git stash -q && git switch -q main
git rebase main feature-mocha
git branch --show-current
git log --oneline main..feature-mocha
git stash pop -q
```

```text
Current branch feature-mocha is up to date.
feature-mocha
6f33f8c (HEAD -> feature-mocha) Add mocha special
```

`git rebase BASE BRANCH` checks BRANCH out first; it is left checked out afterwards.

</details>
