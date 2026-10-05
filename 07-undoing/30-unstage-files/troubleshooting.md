<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 30 · Unstage files · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Unstage the file in a brand-new repository, before the first commit:

```bash
mkdir -p ~/git-practice/lesson-30-new && cd ~/git-practice/lesson-30-new && git init -q
echo hello > hello.txt && git add hello.txt
git restore --staged hello.txt 2>&1
```

```text
fatal: could not resolve 'HEAD'
```

## Troubleshoot

`could not resolve 'HEAD'`: `git restore --staged` copies the version from `HEAD`, and a new repository has no commit yet.
`git status` itself tells you what to use instead:

```bash
cd ~/git-practice/lesson-30-new
git status | grep -A1 "Changes to be committed"
```

```text
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
```

## Fix

```bash
git rm -q --cached hello.txt
git status --short
cd ~/git-practice/lesson-30
```
