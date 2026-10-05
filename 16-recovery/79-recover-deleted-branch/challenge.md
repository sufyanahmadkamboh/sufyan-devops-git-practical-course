<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 79 · Recover a deleted branch · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Protect yourself: make Git keep unreachable objects for 90 days in this clone, and show the setting.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-79/grace
git config gc.pruneExpire 90.days.ago
git config gc.reflogExpireUnreachable 90.days.ago
git config --get gc.pruneExpire
```

```text
90.days.ago
```

The defaults are 2 weeks (`gc.pruneExpire`) and 30 days (`gc.reflogExpireUnreachable`).

</details>
