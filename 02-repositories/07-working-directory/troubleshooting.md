<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 07 · The working directory · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

You worked for an hour and want everything back the way it was, so you delete the folder's files by hand and copy
old ones from somewhere. Simulate a simpler version: you edited a file and now want the committed version, but you
type the wrong command:

```bash
git restore menu.text 2>&1
```

```text
error: pathspec 'menu.text' did not match any file(s) known to git
```

## Troubleshoot

`pathspec 'menu.text' did not match any file(s) known to git`: the path is wrong (`.text` instead of `.txt`). Git can
only restore paths it knows. List what it tracks:

```bash
git ls-files
```

## Fix

```bash
git restore menu.txt prices.txt
git add -A && git status --short
```

```text
R  README.md -> INFO.md
A  hours.txt
```

`menu.txt` and `prices.txt` are back to their committed content. And after `git add -A`, the rename from the exercise
is recognised: `R README.md -> INFO.md`.
