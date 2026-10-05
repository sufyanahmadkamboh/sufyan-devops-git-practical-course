<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 13 · git log · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Look for a commit you know exists, and see nothing:

```bash
git log --oneline --grep=matcha
```

```text
```

## Troubleshoot

Plain `git log` follows only the **current branch** (`HEAD`). The matcha commit is on `feature-tea`, which `main`
does not contain. When a commit seems to be missing, ask: which branch am I on, and is the commit on another branch?

```bash
git status | head -1
git branch
```

## Fix

```bash
git log --oneline --all --grep=matcha
git branch --contains "$(git log --all --format=%h --grep=matcha)"
```

```text
5b84357 (feature-tea) Add matcha
  feature-tea
```

`--all` searches every branch, and `git branch --contains` names the branch that has the commit.
