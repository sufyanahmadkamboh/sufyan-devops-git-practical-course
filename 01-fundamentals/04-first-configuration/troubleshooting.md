<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 04 · First Git configuration · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A fresh machine (or a new CI runner) with no identity at all. Simulate it by hiding the global file for one command:

```bash
cd ~/git-practice/lesson-04
echo "test" > note.txt && git add note.txt
GIT_CONFIG_GLOBAL=/dev/null git -c user.useConfigOnly=true commit -m "First note" 2>&1
```

```text
Author identity unknown

*** Please tell me who you are.

Run

...
```

## Troubleshoot

`Please tell me who you are` / `Author identity unknown`: no `user.name` or `user.email` at any level. Check what Git
can see:

```bash
GIT_CONFIG_GLOBAL=/dev/null git config --show-origin --get user.email || echo "no identity at any level"
```

## Fix

Configure the identity (globally on your own machine; in CI, set it in the job). Then the commit works:

```bash
git config --global user.email >/dev/null && git commit -q -m "First note" && git log --format='%h %an <%ae> %s'
```

```text
fa836d9 Ada Lovelace <ada@example.com> First note
```
