<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 50 · SSH vs HTTPS · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Write a one-liner that tells you whether the current clone uses SSH or HTTPS.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-50
case "$(git remote get-url origin)" in https://*) echo HTTPS ;; git@*|ssh://*) echo SSH ;; *) echo other ;; esac
```

```text
HTTPS
```

</details>
