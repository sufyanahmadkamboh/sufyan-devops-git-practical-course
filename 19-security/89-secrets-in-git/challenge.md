<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 89 · Secrets in Git · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Find the commit that **introduced** the token, by its value, with the pickaxe search.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-89/eve
git log --oneline -S "cafe_token_" --all
```

```text
7b0796b (HEAD -> main, origin/main, origin/HEAD) Remove secrets
a8b2304 Add app configuration
```

`-S` lists commits where the number of occurrences changed: the one that added it and the one that removed it.

</details>
