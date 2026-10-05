<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 72 · Git clean · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

"Make it like a fresh clone", with `-x` and without a preview:

```bash
git clean -f -d -x
```

```text
Removing .env
Removing keep.txt
```

## Troubleshoot

`.env` held local settings and a password that are not in Git (on purpose: lesson 73). `git clean` does not use a
trash bin, the reflog or the stash: the file is gone. Git has no record of it:

```bash
cat .env 2>&1 | sed 's/.*No such file.*/no such file/'
git log --all --oneline -- .env | wc -l
```

## Fix

Recreate it from the documented template (projects keep a `.env.example` for exactly this), and never use `-x` without
`-n` first:

```bash
printf 'DB_PASSWORD=change-me\n' > .env.example && git add .env.example && git commit -q -m "Add .env.example"
cp .env.example .env
git clean -n -d -x
```

```text
Would remove .env
```

The preview now shows `.env` would be removed: you see it **before** it happens.
