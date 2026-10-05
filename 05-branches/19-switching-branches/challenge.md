<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 19 · Switching branches · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Use `git switch` to look at the code as it was on `feature-tea` without being able to commit to the branch by mistake.
(Hint: lesson 78, `--detach`.)

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-19
git switch --detach feature-tea 2>&1
git status | head -1
git switch -q main
```

```text
HEAD is now at bf2e403 Add matcha
HEAD detached at refs/heads/feature-tea
```

A detached `HEAD` points at a commit, not a branch: you can look around, and new commits would not move any branch.

</details>
