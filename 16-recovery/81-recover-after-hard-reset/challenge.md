<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 81 · Recover after a hard reset · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Recover a commit after a reset **and** a second operation (so `ORIG_HEAD` no longer helps).

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-81
git reset -q --hard before-cleanup && git branch -D before-cleanup > /dev/null
git reset -q --hard HEAD~1
git commit -q --allow-empty -m "Something else"
git log --oneline -1 ORIG_HEAD
target=$(git reflog --format='%h %gs' | awk '/commit: Price green tea/ {print $1; exit}')
git branch rescued "$target" && git log --oneline -1 rescued
```

```text
d37a774 Price green tea
d37a774 (rescued) Price green tea
```

`ORIG_HEAD` now points elsewhere; the reflog still lists the "Price green tea" commit.

</details>
