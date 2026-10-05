<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 62 · Rebase vs merge · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show which commits Grace's branch and Ada's branch have in common by patch, even though their IDs differ.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-62-grace
git fetch -q
git log --oneline --cherry-mark --left-right origin/main...HEAD
```

```text
> 3b7ba33 (HEAD -> feature-tea) Add notes
> 507d4af (origin/feature-tea) Price green tea
> 0dda4da Add green tea to the menu
```

`=` marks commits with an equivalent patch on the other side, `<`/`>` the ones unique to each side.

</details>
