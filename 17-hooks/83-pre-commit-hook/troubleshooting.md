<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 83 · Pre-commit hook · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

In a hurry, someone bypasses the hook:

```bash
printf 'debug_key = AKIA%s\n' "IOSFODNN7EXAMPLE" > debug.ini
git add debug.ini
git commit -q --no-verify -m "Add debug settings"
git log --oneline -1
```

```text
a9c217c (HEAD -> main) Add debug settings
```

## Troubleshoot

`--no-verify` skips `pre-commit` entirely, and so does a fresh clone (hooks are not cloned), a GUI client configured
differently, or a commit made on another machine. The secret is now in a commit:

```bash
git show HEAD --stat --format=%s
git show HEAD:debug.ini | sed -E 's/(AKIA....).*/\1…/'
```

```text
Add debug settings

 debug.ini | 1 +
 1 file changed, 1 insertion(+)
debug_key = AKIAIOSF…
```

## Fix

Not pushed yet: remove the file from the commit and from Git's tracking, keep it ignored. (If it had been pushed, the
key must be **revoked** and history cleaned: lessons 89–90.)

```bash
git reset -q --soft HEAD~1
git restore --staged debug.ini && rm debug.ini
echo "debug.ini" >> .gitignore && git add .gitignore && git commit -q -m "Ignore debug.ini"
git log --oneline -1
git ls-files | grep -x debug.ini || echo "debug.ini is not tracked"
```

```text
3ed7a18 (HEAD -> main) Ignore debug.ini
debug.ini is not tracked
```

Prevention at the server: GitHub **push protection** (secret scanning) rejects pushes containing known key formats,
and CI runs the same scanner; neither can be skipped with `--no-verify`.
