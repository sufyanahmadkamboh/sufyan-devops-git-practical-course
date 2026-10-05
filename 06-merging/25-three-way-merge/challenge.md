<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 25 · Three-way merge · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

After the merge, show the changes the merge brought into `main` relative to `main`'s previous tip, using the merge
commit's first parent.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-25
git diff --stat HEAD^1 HEAD
```

```text
 other.txt | 1 +
 1 file changed, 1 insertion(+)
```

`HEAD^1` is the first parent (where `main` was), `HEAD^2` the second (the merged branch).

</details>
