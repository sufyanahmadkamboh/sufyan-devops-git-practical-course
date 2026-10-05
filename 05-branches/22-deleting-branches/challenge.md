<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 22 · Deleting branches · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Delete every local branch that is merged into `main`, except `main` itself, in one command line.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-22
git branch done-1 && git branch done-2
git branch --merged main | grep -vE '^\*|^\s*main$' | xargs -r git branch -d
git branch
```

```text
Deleted branch done-1 (was bb67674).
Deleted branch done-2 (was bb67674).
* main
```

Always run the list (`git branch --merged main`) alone first and read it before piping it into a delete.

</details>
