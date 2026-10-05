<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 25 · Three-way merge · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Merge a branch that is not related to `main` at all: no merge base.

```bash
git switch -q --orphan unrelated && echo "other project" > other.txt && git add other.txt && git commit -q -m "Other project"
git switch -q main
git merge unrelated 2>&1
```

```text
fatal: refusing to merge unrelated histories
```

## Troubleshoot

`refusing to merge unrelated histories`: `unrelated` has no commit in common with `main` (it was started with
`--orphan`), so there is no merge base. In real life this appears when you connect a local project to a GitHub
repository that was created **with** a README (two first commits), or when two different projects are combined.

```bash
git merge-base main unrelated || echo "no merge base"
```

## Fix

If combining them is really intended, allow it explicitly:

```bash
git merge --allow-unrelated-histories --no-edit unrelated
ls
```

```text
Merge made by the 'ort' strategy.
 other.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 other.txt
README.md
menu.txt
other.txt
prices.txt
```
