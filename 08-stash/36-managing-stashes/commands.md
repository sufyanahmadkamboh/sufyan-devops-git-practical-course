<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 36 · Managing stashes · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-36 basic
cd ~/git-practice/lesson-36
for idea in "price draft" "menu ideas"; do
  echo "$idea" >> notes.txt && git add notes.txt && git stash push -q -m "$idea"
done
git stash list
```

## Demonstration

```bash
git stash show -p 'stash@{1}'
```

```bash
git stash branch price-draft 'stash@{1}'
git stash list
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-36
git stash list | wc -l
```

## Break it

```bash
echo "important recipe" > recipe.txt && git add recipe.txt && git stash push -q -m "recipe"
git stash clear
git stash list | wc -l
```

## Troubleshoot

```bash
for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%h %s' "$c"
done | grep "On main"
```

## Fix

```bash
lost=$(for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/On main: recipe/ {print $1}')
git stash apply -q "$lost"
cat recipe.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-36
git stash push -q -m "recipe again"
git stash list --format=%gd | while read -r s; do echo "$s $(git stash show --name-only "$s" | wc -l) file(s)"; done
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-36
```
