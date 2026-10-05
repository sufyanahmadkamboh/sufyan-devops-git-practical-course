<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 68 · Git tags · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Tag a mistake, `v1.0.1` on the wrong commit, then delete it locally before anyone sees it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-68/ada
git tag v1.0.1 d6df412
git tag -d v1.0.1
git tag
```

```text
Deleted tag 'v1.0.1' (was d6df412)
v0.9.0
v1.0.0
```

Once a tag is pushed and others have fetched it, deleting or moving it causes confusion: publish a new version instead.

</details>
