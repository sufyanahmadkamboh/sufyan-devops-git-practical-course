<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 37 · What is a remote? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace commits and pushes. Ada looks at `origin/main`, expecting to see Grace's commit:

```bash
echo "Open 8-18" >> README.md && git commit -q -am "Add opening hours" && git push -q
cd ../ada
git log --oneline -1 origin/main
```

```text
4267004 (HEAD -> main, origin/main, origin/HEAD) Add prices
```

## Troubleshoot

Ada's `origin/main` still shows `Add prices`. Remote-tracking branches are **not live**: they are updated only by
`git fetch`, `git pull` or `git push`. Ada's clone has not talked to the server since Grace pushed.

## Fix

```bash
git fetch
git log --oneline -1 origin/main
```

```text
From ~/git-practice/lesson-37/server/cafe
   4267004..ee8ab62  main       -> origin/main
ee8ab62 (origin/main, origin/HEAD) Add opening hours
```
