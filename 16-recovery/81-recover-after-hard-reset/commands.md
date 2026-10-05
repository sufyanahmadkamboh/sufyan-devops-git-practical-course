<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 81 · Recover after a hard reset · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-81 basic
cd ~/git-practice/lesson-81
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git log --oneline -3
```

## Demonstration

```bash
git reset --hard HEAD~2
git log --oneline -1
```

```bash
git log --oneline -1 ORIG_HEAD
git reflog -3
```

```bash
git reset --hard ORIG_HEAD
git log --oneline -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-81
git log --oneline -1 before-cleanup
git log --oneline -1 main
```

## Break it

```bash
git reset -q --hard before-cleanup
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
git reset --hard
cat menu.txt
```

## Troubleshoot

```bash
git fsck --lost-found 2> /dev/null
```

## Fix

```bash
for f in .git/lost-found/other/*; do
  grep -l "cortado" "$f" > /dev/null 2>&1 && cp "$f" menu.txt && echo "restored from $(basename "$f")"
done
cat menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-81
git reset -q --hard before-cleanup && git branch -D before-cleanup > /dev/null
git reset -q --hard HEAD~1
git commit -q --allow-empty -m "Something else"
git log --oneline -1 ORIG_HEAD
target=$(git reflog --format='%h %gs' | awk '/commit: Price green tea/ {print $1; exit}')
git branch rescued "$target" && git log --oneline -1 rescued
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-81
```
