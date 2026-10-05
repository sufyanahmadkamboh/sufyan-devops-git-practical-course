<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 08 · git status · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create a state where `git status --short` shows `A ` (a new file staged), ` D` (a deleted tracked file, not staged)
and `??` (an untracked file) at the same time.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-08/ada
echo "2 for 1" > specials.txt && git add specials.txt
rm README.md
echo "todo" > notes.txt
git status --short
```

```text
 D README.md
A  specials.txt
?? notes.txt
```

</details>
