<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 60 · What is rebase? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Rebase `feature-tea` back onto the original base commit `4267004` ("Add prices") using `--onto`, removing everything
`main` added from under it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-60
git rebase -q --onto 4267004 main feature-tea
git log --oneline --graph -3
```

```text
* ad12083 (HEAD -> feature-tea) Add green tea to the menu
* 4267004 Add prices
* fc345e6 Add the menu
```

`git rebase --onto NEW OLD BRANCH` replays the commits of BRANCH after OLD onto NEW.

</details>
