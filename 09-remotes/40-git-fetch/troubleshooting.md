<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 40 · git fetch · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace deletes a branch on the server; Ada's clone keeps showing it:

```bash
cd ../grace && git push -q origin main:old-promo && cd ../ada && git fetch -q
cd ../grace && git push -q origin --delete old-promo && cd ../ada
git fetch
git branch -r
```

```text
  origin/HEAD -> origin/main
  origin/main
  origin/old-promo
```

## Troubleshoot

`origin/old-promo` is stale: a plain fetch adds and updates remote-tracking branches but never deletes them. On busy
repositories this produces dozens of dead `origin/*` branches.

```bash
git remote show origin | grep -i stale
```

```text
    refs/remotes/origin/old-promo stale (use 'git remote prune' to remove)
```

## Fix

```bash
git fetch --prune
git branch -r
```

```text
From ~/git-practice/lesson-40/server/cafe
 - [deleted]         (none)     -> origin/old-promo
  origin/HEAD -> origin/main
  origin/main
```

Make it permanent: `git config --global fetch.prune true`.
