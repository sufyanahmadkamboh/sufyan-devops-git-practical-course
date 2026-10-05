<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 03 · Installing Git · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Call a Git command that does not exist, the classic typo:

```bash
git comit -m "test" 2>&1
```

```text
git: 'comit' is not a git command. See 'git --help'.

The most similar command is
	commit
```

## Troubleshoot

Git says it is not a command and usually suggests the closest real one. The same message appears for commands that
come from an extension you have not installed (`git lfs` without Git LFS, `git filter-repo` without filter-repo).

## Fix

Use the right name. To catch typos automatically, Git can run the closest match after a short delay:

```bash
git config --global help.autocorrect prompt
git config --global --get-regexp '^help\.'
```

`prompt` asks before running the guess. Many people prefer leaving this off: a typo should fail loudly.
