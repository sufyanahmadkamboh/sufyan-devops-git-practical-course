<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 96 · Projects · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-96 github
cd ~/git-practice/lesson-96
```

```bash
gh auth status --active 2>&1 | grep -i scopes
```

## Demonstration

```bash
me=$(gh api user --jq .login)
number=$(gh project create --owner "$me" --title "Cafe roadmap" --format json --jq .number)
issue_url=$(gh issue create --title "Update the menu board" --body "New board for v1.1.0." )
gh project item-add "$number" --owner "$me" --url "$issue_url"
gh project item-list "$number" --owner "$me" --format json --jq '.items[] | "\(.content.title): \(.status)"'
```

## Hands-on exercise

```bash
me=$(gh api user --jq .login)
gh project list --owner "$me" --format json --jq '.projects[].title'
```

## Break it

```bash
gh project list --owner "$(gh api user --jq .login)" 2>&1
```

## Fix

```bash
gh auth refresh -h github.com -s project
gh project list --owner "$(gh api user --jq .login)"
```

## Practice challenge

```bash
gh api -i user 2>/dev/null | grep -i "^x-oauth-scopes"
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-96
```
