<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 34 · What is a stash? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Is a stash pushed with `git push`? Find out by inspecting what a stash really is.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-34
git stash -q
git show-ref | grep stash
git log --oneline -1 stash
git stash pop -q
```

```text
b772b00c744a1737f6368305820a13d2af328644 refs/stash
b772b00 (refs/stash) WIP on main: 8c1f1e8 Fix the espresso price
```

A stash is a special commit stored under `refs/stash`, a local reference. `git push` sends branches and tags, never
`refs/stash`: stashes stay on your computer.

</details>
