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
ee1dab5fd68598b43d281c1d9a045001eb9f0c78 refs/stash
ee1dab5 (refs/stash) WIP on main: c9d93e6 Fix the espresso price
```

A stash is a special commit stored under `refs/stash`, a local reference. `git push` sends branches and tags, never
`refs/stash`: stashes stay on your computer.

</details>
