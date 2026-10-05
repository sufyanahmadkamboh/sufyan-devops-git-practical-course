<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 93 · GitHub Issues · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-93 github
cd ~/git-practice/lesson-93
```

## Demonstration

```bash
gh issue create --title "Green tea has no price" \
  --body "Green tea is on the menu, but prices.txt has no line for it. Customers cannot order it."
```

```bash
gh issue list --state open --json number,title,state \
  --jq '.[] | select(.title == "Green tea has no price") | "#\(.number) \(.title) [\(.state)]"'
```

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Green tea has no price")][0].number')
echo "green tea 2.80" >> prices.txt
git commit -q -am "Price green tea (fixes #$n)"
git push 2>&1 | tail -1
```

```bash
gh issue list --state all --json number,title,state \
  --jq '[.[] | select(.title == "Green tea has no price")][0] | "#\(.number) \(.state)"'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-93
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --comments | tail -4
```

## Break it

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
git switch -q -c add-chai
echo "chai" >> menu.txt && git commit -q -am "Add chai (closes #$n)"
git push -q -u origin add-chai 2> /dev/null
git log --oneline -1
```

```bash
sleep 5
n=$(gh issue list --state all --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --json state --jq .state
```

## Fix

```bash
git switch -q main && git pull -q && git merge -q --no-edit add-chai && git push -q 2> /dev/null
git push -q origin --delete add-chai 2> /dev/null
```

```bash
n=$(gh issue list --state all --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --json state --jq .state
```

## Practice challenge

```bash
cd ~/git-practice/lesson-93
gh issue list --state closed --limit 50 --json number,title,stateReason \
  --jq '[.[] | select(.title == "Green tea has no price" or .title == "Add chai to the menu")] | unique_by(.title)[] | "#\(.number) \(.title): \(.stateReason)"'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-93
```
