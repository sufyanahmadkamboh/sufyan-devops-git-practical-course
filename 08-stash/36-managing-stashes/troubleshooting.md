<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 36 · Managing stashes · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Clear the shelf, then realise one stash was still needed:

```bash
echo "important recipe" > recipe.txt && git add recipe.txt && git stash push -q -m "recipe"
git stash clear
git stash list | wc -l
```

## Troubleshoot

`git stash clear` removed the `refs/stash` entries, but stashes are commits: the objects are still in the repository
until Git's garbage collection removes unreachable objects. `git fsck` lists unreachable commits; stash commits have
the message `On <branch>: <message>`:

```bash
for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%h %s' "$c"
done | grep "On main"
```

```text
5545d62 On main: price draft
186e3ba On main: recipe
62fcf1b On main: menu ideas
```

## Fix

```bash
lost=$(for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/On main: recipe/ {print $1}')
git stash apply -q "$lost"
cat recipe.txt
```

```text
important recipe
```
