<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 76 · HEAD · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-76 feature
cd ~/git-practice/lesson-76
```

## Demonstration

```bash
cat .git/HEAD
git symbolic-ref HEAD
git rev-parse HEAD
```

```bash
git switch -q feature-tea
cat .git/HEAD
git rev-parse --short HEAD
```

```bash
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
cat .git/HEAD
echo "feature-tea: $(git rev-parse --short feature-tea), HEAD: $(git rev-parse --short HEAD)"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-76
git log -1 --format=%s HEAD~2
```

## Break it

```bash
echo "ref: refs/heads/mian" > .git/HEAD
git status 2>&1 | head -3
```

## Troubleshoot

```bash
git branch
```

## Fix

```bash
git symbolic-ref HEAD refs/heads/feature-tea
git symbolic-ref HEAD
git status --short | wc -l
```

## Practice challenge

```bash
cd ~/git-practice
git clone -q lesson-76 lesson-76-clone
git -C lesson-76-clone symbolic-ref refs/remotes/origin/HEAD
git -C lesson-76-clone branch --show-current
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-76 ~/git-practice/lesson-76-clone
```
