<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 71 · Git blame · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-71 conflict
cd ~/git-practice/lesson-71
```

## Demonstration

```bash
git blame prices.txt
```

```bash
git blame -L 2,2 prices.txt
git show --stat "$(git blame -L 2,2 --porcelain prices.txt | head -1 | cut -c1-7)" | head -6
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-71
git log --oneline -L 2,2:prices.txt | grep -E "^[0-9a-f]{7} "
```

## Break it

```bash
awk '{printf "%-12s %s\n", $1, $2}' prices.txt > p.tmp && mv p.tmp prices.txt
git commit -q -am "Align the prices"
git log --oneline -1
git blame prices.txt
```

## Fix

```bash
git rev-parse HEAD > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
git blame prices.txt
git log --oneline -1 "$(git blame -L 2,2 --porcelain prices.txt | head -1 | cut -c1-40)"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-71
git blame --line-porcelain prices.txt | sed -n 's/^author //p' | sort | uniq -c
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-71
```
