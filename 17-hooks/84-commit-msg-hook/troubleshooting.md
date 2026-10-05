<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 84 · Commit message hook · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

```bash
echo "mocha" >> menu.txt
git commit -am "fixed stuff" 2>&1
```

```text
commit-msg: "fixed stuff" does not follow Conventional Commits
  expected: type(scope): description   e.g. feat(menu): add green tea
```

## Troubleshoot

The hook printed why: no type prefix. The commit was not created and nothing is lost: the change is still staged and
modified, ready for a second try.

```bash
git status --short
```

```text
 M menu.txt
```

## Fix

```bash
git commit -q -am "feat(menu): add mocha"
git log --oneline -1
```
