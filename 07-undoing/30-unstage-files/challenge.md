<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 30 · Unstage files · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Stage everything, unstage everything, and prove that no edit was lost.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-30
git add .
git restore --staged .
git status --short
git diff --stat
```

```text
 M prices.txt
?? notes.txt
 prices.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

</details>
