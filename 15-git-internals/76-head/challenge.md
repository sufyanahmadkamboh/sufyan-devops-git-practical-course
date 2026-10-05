<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 76 · HEAD · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Clone the lab repository and show what the clone's `origin/HEAD` points to. Why that branch?

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice
git clone -q lesson-76 lesson-76-clone
git -C lesson-76-clone symbolic-ref refs/remotes/origin/HEAD
git -C lesson-76-clone branch --show-current
```

```text
refs/remotes/origin/feature-tea
feature-tea
```

`origin/HEAD` records the **source's** `HEAD` at clone time: the lab was on `feature-tea`, so the clone checked out
`feature-tea` and considers it the default branch. On GitHub, the source's `HEAD` is the repository's default branch.

</details>
