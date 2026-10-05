<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 15 · git diff · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Compare against a branch name with a typo:

```bash
git diff main..featur-tea 2>&1
```

```text
fatal: ambiguous argument 'main..featur-tea': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

## Troubleshoot

`ambiguous argument 'featur-tea': unknown revision or path not in the working tree`: Git could not resolve the name
as a commit, branch, tag or file. List the real branch names:

```bash
git branch --all
```

## Fix

```bash
git diff main..feature-tea -- menu.txt
```
