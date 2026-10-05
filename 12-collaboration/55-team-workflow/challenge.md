<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 55 · Team Git workflow · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show, for each developer's clone, how many commits its `main` is behind the server.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-55
for dev in ada grace linus; do
  git -C "$dev" fetch -q
  echo "$dev: $(git -C "$dev" rev-list --count main..origin/main) behind"
done
```

```text
ada: 2 behind
grace: 1 behind
linus: 0 behind
```

</details>
