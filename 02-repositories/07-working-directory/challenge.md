<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 07 · The working directory · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make `git status --short` show exactly one modified file and one untracked file, and nothing else.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-07
git restore --staged . && git restore . && rm -f INFO.md hours.txt && git checkout -q -- README.md 2>/dev/null; git status --short
echo "chai" >> menu.txt
echo "Monday: 2 for 1" > specials.txt
git status --short
```

```text
 M menu.txt
?? specials.txt
```

</details>
