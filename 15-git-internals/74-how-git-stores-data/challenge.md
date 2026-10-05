<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 74 · How Git stores data · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Commit a copy of `menu.txt` under another name. How many new blobs does that create?

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-74
cp menu.txt menu-copy.txt && git add menu-copy.txt && git commit -q -m "Copy the menu"
[ "$(git rev-parse HEAD:menu.txt)" = "$(git rev-parse HEAD:menu-copy.txt)" ] && echo "same blob: no new blob, only a new tree and commit"
```

```text
same blob: no new blob, only a new tree and commit
```

</details>
