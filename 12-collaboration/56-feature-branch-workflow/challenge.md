<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 56 · Feature branch workflow · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Write a one-liner that lists remote branches whose last commit is older than 14 days (stale branches to clean up).

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-56/ada
git fetch -q
git for-each-ref refs/remotes/origin --format='%(committerdate:unix) %(refname:short)' |
  awk -v limit="$(( $(date +%s) - 14*24*3600 ))" '$1 < limit {print $2}'
```

```text
```

Branches created by the lab script's fixed 2026-01-05 commits (such as `origin/main` before today's work) would appear;
everything committed today does not.

</details>
