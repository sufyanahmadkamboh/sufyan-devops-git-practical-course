<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 73 · .gitignore · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Ignore everything in `logs/` except a `README.md` that explains the folder.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-73
echo "Application logs are written here." > logs/README.md
printf 'logs/*\n!logs/README.md\n' >> .gitignore
git add . && git commit -q -m "Keep logs/README.md"
git ls-files logs
```

```text
logs/README.md
```

`logs/*` (not `logs/`) ignores the contents but not the folder, so the `!` exception can work.

</details>
