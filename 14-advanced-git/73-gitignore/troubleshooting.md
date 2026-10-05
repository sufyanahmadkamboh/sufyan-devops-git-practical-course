<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 73 · .gitignore · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A config file was committed long ago; now someone adds it to `.gitignore`:

```bash
echo "debug=false" > config.local && git add config.local && git commit -q -m "Add config"
echo "config.local" >> .gitignore && git commit -q -am "Ignore config.local"
echo "debug=true" > config.local
git status --short
```

```text
 M config.local
```

## Troubleshoot

`M config.local`: still tracked, still showing changes. `.gitignore` only affects **untracked** files; Git keeps
tracking every file that is already in the index.

```bash
git ls-files | grep config
```

```text
config.local
```

## Fix

Remove it from the index (not from disk), commit, and it becomes an ignored file:

```bash
git rm -q --cached config.local
git commit -q -m "Stop tracking config.local"
git status --short --ignored | grep config
cat config.local
```

```text
!! config.local
debug=true
```

If the file contained **secrets**, this is not enough: they are still in the history (lesson 90), so rotate them.
