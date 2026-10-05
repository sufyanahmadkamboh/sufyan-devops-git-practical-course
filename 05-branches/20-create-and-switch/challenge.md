<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 20 · Create and switch in one command · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create `release-test` from the commit **two before** the tip of `main`, in one command.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-20
git switch -c release-test main~2
git log --oneline -1
```

```text
Switched to a new branch 'release-test'
fc345e6 (HEAD -> release-test) Add the menu
```

</details>
