<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 48 · HTTPS authentication · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-48 basic
cd ~/git-practice/lesson-48
```

```bash
me=$(gh api user --jq .login)
git remote add origin "https://github.com/$me/git-practice-cafe.git"
git config --show-origin --get-regexp '^credential' || echo "no credential helper configured"
```

## Demonstration

```bash
git ls-remote --heads origin
```

```bash
git push --dry-run origin main 2>&1
```

## Hands-on exercise

```bash
git config --show-origin --get-all credential.https://github.com.helper
```

## Break it

```bash
me=$(gh api user --jq .login)
git push --dry-run "https://$me:my-account-password@github.com/$me/git-practice-cafe.git" main 2>&1
```

## Fix

```bash
gh auth setup-git
git push --dry-run origin main:refs/heads/lesson-48-check 2>&1
```

## Practice challenge

```bash
gh auth status --active 2>&1 | grep -i scopes
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-48
```
