<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 06 · git init · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
mkdir -p ~/git-practice/lesson-06 && cd ~/git-practice/lesson-06
pwd
```

## Demonstration

```bash
mkdir git-demo
cd git-demo
git init
```

```bash
git status
```

```bash
cat .git/HEAD
ls .git/refs/heads/ | wc -l
```

```bash
echo "# Demo" > README.md
git status --short
git status | sed -n '1,6p'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-06/notes
git status | head -1
```

## Break it

```bash
cd ~/git-practice/lesson-06
mkdir -p home-sim/projects/website && cd home-sim
git init -q
cd projects/website
echo "<h1>Hi</h1>" > index.html
git status --short
git rev-parse --show-toplevel
```

## Fix

```bash
cd ~/git-practice/lesson-06/home-sim
ls -A
rm -rf .git
cd projects/website && git init -q
git rev-parse --show-toplevel
```

## Practice challenge

```bash
cd ~/git-practice/lesson-06/git-demo
git add README.md && git commit -q -m "First commit"
git init
git log --oneline
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-06
```
