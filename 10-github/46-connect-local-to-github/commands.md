<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 46 · Connecting local Git to GitHub · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-46 basic
cd ~/git-practice/lesson-46
git log --oneline
```

```bash
me=$(gh api user --jq .login)
echo "$me"
```

## Demonstration

```bash
me=$(gh api user --jq .login)
git remote add origin "https://github.com/$me/git-practice-cafe.git"
git remote -v
```

```bash
git push -u origin main
```

```bash
git fetch -q
git log --oneline --reverse origin/main | head -3
```

## Hands-on exercise

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/contents" --jq '.[].name'
```

## Break it

```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practise-cafe.git"
git ls-remote origin 2>&1
```

## Troubleshoot

```bash
git remote get-url origin
```

## Fix

```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practice-cafe.git"
git ls-remote --heads origin
```

## Practice challenge

```bash
cd ~/git-practice/lesson-46
git switch -q -c docs
git push -q -u origin docs 2>&1
git ls-remote --heads origin
git push -q origin --delete docs 2>&1
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-46
```
