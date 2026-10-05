<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 26 · Merge conflicts · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Set `zdiff3` as your conflict style globally, recreate the conflict, and show that the base appears automatically.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-26
git config --global merge.conflictStyle zdiff3
git merge feature-tea > /dev/null 2>&1 || true
cat prices.txt
git merge --abort
```

```text
espresso 2.50
<<<<<<< HEAD
latte 3.30
||||||| 4267004
latte 3.20
=======
latte 3.50
>>>>>>> feature-tea
cappuccino 3.40
```

`zdiff3` is `diff3` with identical lines at the edges moved out of the conflict: a smaller conflict to read.

</details>
