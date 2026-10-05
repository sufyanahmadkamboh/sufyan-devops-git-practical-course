<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 38 · git remote · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-38 remote
cd ~/git-practice/lesson-38
git clone -q --bare server/cafe.git upstream.git
cd ada
```

## Demonstration

```bash
git remote add upstream ../upstream.git
git remote -v
git fetch -q upstream
git branch -r
```

```bash
mv ../server/cafe.git ../server/cafe-shop.git
git remote set-url origin ../server/cafe-shop.git
git remote -v | grep origin
git fetch origin && echo "fetch ok"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-38/ada
git branch -r
```

## Break it

```bash
git remote add origin ../server/cafe-shop.git 2>&1
```

## Troubleshoot

```bash
git remote get-url origin
```

## Fix

```bash
git remote set-url origin ../server/cafe-shop.git
git remote -v
```

## Practice challenge

```bash
cd ~/git-practice/lesson-38/ada
git remote remove original
git remote
git branch -r
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-38
```
