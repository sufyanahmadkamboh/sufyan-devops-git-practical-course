<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 40 · git fetch · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make a commit on Ada's `main` without pushing, fetch, and show both the incoming and the outgoing commits.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-40/ada
echo "note" > notes.txt && git add notes.txt && git commit -q -m "Ada's unpushed note"
git fetch -q
echo "incoming:"; git log --oneline main..origin/main
echo "outgoing:"; git log --oneline origin/main..main
```

```text
incoming:
outgoing:
0ca2024 (HEAD -> main) Ada's unpushed note
```

</details>
