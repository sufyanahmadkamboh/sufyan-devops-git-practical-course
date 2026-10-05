<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 28 · Aborting a merge · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

How can you tell, from the command line only, whether a merge is currently in progress? Write a one-line check.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-28
git restore prices.txt
git merge feature-tea > /dev/null 2>&1 || true
git rev-parse -q --verify MERGE_HEAD > /dev/null && echo "merge in progress" || echo "no merge"
git merge --abort
```

```text
merge in progress
```

</details>
