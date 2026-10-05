<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 45 · Creating a GitHub repository · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
gh auth status --active 2>&1 | grep -E "Logged in|scopes"
```

## Demonstration

```bash
gh repo create git-practice-cafe --public --description "Practice repository for the Git Practical Course"
```

```bash
gh repo view git-practice-cafe --json name,visibility,url --jq '"\(.name) \(.visibility) \(.url)"'
```

## Hands-on exercise

```bash
gh repo view git-practice-cafe --json isEmpty,defaultBranchRef
```

## Break it

```bash
gh repo create git-practice-cafe --public 2>&1
```

## Fix

```bash
gh repo list --limit 100 --json name --jq '.[].name' | grep -x git-practice-cafe
```

## Practice challenge

```bash
me=$(gh api user --jq .login)
gh repo edit "$me/git-practice-cafe" --add-topic git --add-topic practice > /dev/null
gh repo view git-practice-cafe --json repositoryTopics --jq '[.repositoryTopics[].name] | join(", ")'
```
