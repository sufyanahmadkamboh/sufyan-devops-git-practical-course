<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 40 · git fetch · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-40 remote
cd ~/git-practice/lesson-40/grace
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git push -q
cd ../ada
```

## Demonstration

```bash
git fetch
```

```bash
git status
git log --oneline main..origin/main
```

```bash
git diff main origin/main
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-40/ada
git status
```

## Break it

```bash
cd ../grace && git push -q origin main:old-promo && cd ../ada && git fetch -q
cd ../grace && git push -q origin --delete old-promo && cd ../ada
git fetch
git branch -r
```

## Troubleshoot

```bash
git remote show origin | grep -i stale
```

## Fix

```bash
git fetch --prune
git branch -r
```

## Practice challenge

```bash
cd ~/git-practice/lesson-40/ada
echo "note" > notes.txt && git add notes.txt && git commit -q -m "Ada's unpushed note"
git fetch -q
echo "incoming:"; git log --oneline main..origin/main
echo "outgoing:"; git log --oneline origin/main..main
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-40
```
