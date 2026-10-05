<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 78 · Detached HEAD · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Detach at `HEAD~2`, make a commit, and **before** leaving, turn it into a branch with one command.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-78
git switch -q --detach HEAD~2
echo "idea" > idea.txt && git add idea.txt && git commit -q -m "Try an idea"
git switch -c experiment
git status | head -1
```

```text
Switched to a new branch 'experiment'
On branch experiment
```

</details>
