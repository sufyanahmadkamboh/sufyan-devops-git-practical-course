<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 03 · Installing Git · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without opening a browser or the internet, find in Git's built-in help the `git commit` option that **changes the
last commit** instead of creating a new one, and the one that **stages all modified files** automatically.

<details>
<summary>Solution</summary>

```bash
git commit -h 2>&1 | grep -E -- '--amend|-a, --all'
```

```text
usage: git commit [-a | --interactive | --patch] [-s] [-v] [-u[<mode>]] [--amend]
    --[no-]reset-author   the commit is authored by me now (used with -C/-c/--amend)
```

`-h` prints the short usage of any command in the terminal; `git help commit` opens the full manual.

</details>
