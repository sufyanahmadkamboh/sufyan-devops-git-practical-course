<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 23 · What is a merge? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Merge in the wrong direction: you meant to bring `main` into your feature branch, but you are on `main`.

```bash
git merge feature-tea
```

```text
Already up to date.
```

## Troubleshoot

`Already up to date.`: `main` already contains everything of `feature-tea` (the merge you just did). The direction
matters: `git merge X` changes the **current** branch. To update `feature-tea` with `main`'s latest work, you must be
**on** `feature-tea`.

## Fix

```bash
git switch -q feature-tea
git merge main
git log --oneline -1
```

```text
Updating bb67674..b328274
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
b328274 (HEAD -> feature-tea, main) Merge branch 'feature-tea'
```

`feature-tea` now has `main`'s work too. (It was a fast-forward: lesson 24.)
