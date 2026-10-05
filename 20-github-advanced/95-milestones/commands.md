<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 95 · Milestones · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-95 github
cd ~/git-practice/lesson-95
```

## Demonstration

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" -f title="v1.1.0" -f description="Chai and the new menu board" \
  -f due_on="2026-12-31T23:59:59Z" --jq '"\(.title) due \(.due_on[:10]): \(.description)"'
```

```bash
for t in "Add chai" "Price chai" "Update the menu board"; do
  gh issue create --title "$t" --body "Part of v1.1.0." --milestone "v1.1.0" > /dev/null
done
```

```bash
gh issue list --milestone "v1.1.0" --json title --jq 'length'
```

```bash
for t in "Add chai" "Price chai"; do
  n=$(gh issue list --milestone "v1.1.0" --state open --json number,title --jq "[.[] | select(.title == \"$t\")][0].number")
  gh issue close "$n" > /dev/null
done
```

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" --jq '.[] | select(.title=="v1.1.0") | "\(.closed_issues) of \(.open_issues + .closed_issues) closed"'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-95
gh issue list --milestone "v1.1.0" --state open --json title --jq '.[].title'
```

## Break it

```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1" 2>&1
```

## Troubleshoot

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" --jq '.[].title'
```

## Fix

```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1.0"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-95
for n in $(gh issue list --milestone "v1.1.0" --state open --json number --jq '.[].number'); do gh issue close "$n" > /dev/null; done
me=$(gh api user --jq .login)
m=$(gh api "repos/$me/git-practice-cafe/milestones" --jq '.[] | select(.title=="v1.1.0") | .number')
gh api -X PATCH "repos/$me/git-practice-cafe/milestones/$m" -f state=closed --jq '"\(.title): \(.state)"'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-95
```
