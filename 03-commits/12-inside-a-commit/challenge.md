<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 12 · What actually happens during a commit? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show that two different commits can share an identical file version: find the `blob` ID of `README.md` in the first
commit and in the latest commit.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-12
git rev-parse "$(git rev-list --max-parents=0 HEAD):README.md"
git rev-parse HEAD:README.md
```

```text
af07f28d5cff41687d90ff3f650baedef059f12e
af07f28d5cff41687d90ff3f650baedef059f12e
```

Same ID: the README never changed, so every snapshot points at the same stored blob.

</details>
