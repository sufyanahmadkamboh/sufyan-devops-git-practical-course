<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 80 · Recover a deleted commit · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Find out how old the oldest entry in this repository's reflog is, and what the configured expiry is.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-80
git reflog --date=relative | tail -1 | sed -E 's/\{[0-9]+ (seconds?|minutes?) ago\}/{N seconds ago}/'
git config --get gc.reflogExpire || echo "gc.reflogExpire not set: default 90 days"
```

```text
3685547 (HEAD -> main, origin/main) HEAD@{N seconds ago}: reset: moving to origin/main
gc.reflogExpire not set: default 90 days
```

</details>
