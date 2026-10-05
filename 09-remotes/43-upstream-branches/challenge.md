<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 43 · Upstream branches · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create `hotfix` from `origin/main`, check its upstream, and change it to `origin/hotfix` after pushing.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-43/ada
git switch -q -c hotfix origin/main
git branch -vv | grep hotfix
git push -q -u origin hotfix
git branch -vv | grep hotfix
```

```text
* hotfix        4267004 [origin/main] Add prices
* hotfix        4267004 [origin/hotfix] Add prices
```

</details>
