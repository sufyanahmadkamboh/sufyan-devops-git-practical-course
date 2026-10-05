<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 72 · Git clean · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Delete only ignored files (build caches), keeping your untracked work.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-72
echo "my work" > work.txt
git clean -f -X
ls
```

```text
Removing .env
README.md
menu.txt
prices.txt
work.txt
```

</details>
