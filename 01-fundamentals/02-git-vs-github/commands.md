<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 02 · Git vs GitHub · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-02 basic
cd ~/git-practice/lesson-02
```

## Demonstration

```bash
git log --oneline
git remote -v
echo "remotes: $(git remote | wc -l)"
```

```bash
git init -q --bare -b main ~/git-practice/lesson-02-server/cafe.git
git remote add origin ~/git-practice/lesson-02-server/cafe.git
git push origin main 2>&1
```

```bash
git ls-remote --heads https://github.com/git/git | head -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-02
git log --oneline -1
git --git-dir ~/git-practice/lesson-02-server/cafe.git log --oneline -1
```

## Break it

```bash
cd ~/git-practice/lesson-02
git remote add backup ~/git-practice/no-such-server/cafe.git
git push backup main 2>&1
```

## Troubleshoot

```bash
git remote -v
```

## Fix

```bash
git remote remove backup
git remote -v
git push origin main 2>&1 | tail -1 || true
git init -q --bare -b main ~/git-practice/lesson-02-backup.git
git remote add backup ~/git-practice/lesson-02-backup.git
git push backup main 2>&1
```

## Practice challenge

```bash
git ls-remote --symref https://github.com/git/git HEAD
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-02 ~/git-practice/lesson-02-server ~/git-practice/lesson-02-backup.git
```
