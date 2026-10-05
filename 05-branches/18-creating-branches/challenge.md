<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 18 · Creating branches · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create a branch called `before-prices` at the commit **before** prices were added, using the commit message to find it,
not a count like `HEAD~1`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-18
git branch before-prices "$(git log --format=%h --grep='Add the menu')"
git branch -v
```

```text
  before-prices fc345e6 Add the menu
  feature/login 4267004 Add prices
  fix-prices    4267004 Add prices
  hotfix-prices fc345e6 Add the menu
* main          4267004 Add prices
```

</details>
