<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 13 · git log · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Print the history as `<short id> | <author> | <relative date> | <subject>`, only for commits that changed `menu.txt`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-13
git log --format='%h | %an | %ar | %s' -- menu.txt
```

```text
2c389c0 | Ada Lovelace | 9 months ago | Add mocha
6833580 | Ada Lovelace | 9 months ago | Add green tea
fc345e6 | Ada Lovelace | 9 months ago | Add the menu
```

</details>
