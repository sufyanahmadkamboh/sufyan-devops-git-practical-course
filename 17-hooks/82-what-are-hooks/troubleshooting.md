<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 82 · What are Git hooks? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A colleague writes a `pre-commit` hook that should block commits containing `TODO`, saving it as a nicely named
script file:

```bash
cat > .git/hooks/pre-commit.sh << 'EOF'
#!/bin/sh
if git diff --cached | grep -q "^+.*TODO"; then echo "pre-commit: remove the TODO first"; exit 1; fi
EOF
chmod +x .git/hooks/pre-commit.sh
echo "TODO: add prices for tea" >> menu.txt && git commit -q -am "Add a TODO" && git log --oneline -1
```

```text
6760c7b (HEAD -> main) Add a TODO
```

## Troubleshoot

The commit went through: the hook never ran. Git looks for a file named exactly `pre-commit`; `pre-commit.sh` is just a
file. Ask Git:

```bash
git hook run pre-commit 2>&1
```

```text
error: cannot find a hook named pre-commit
```

## Fix

Rename it, undo the bad commit, and try again:

```bash
mv .git/hooks/pre-commit.sh .git/hooks/pre-commit
git reset -q --soft HEAD~1
git commit -m "Add a TODO" 2>&1
```

```text
pre-commit: remove the TODO first
```

The hook ran and blocked the commit (exit status 1).
