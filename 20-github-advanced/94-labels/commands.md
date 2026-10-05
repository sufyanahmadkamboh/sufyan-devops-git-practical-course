<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 94 · Labels · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-94 github
cd ~/git-practice/lesson-94
```

## Demonstration

```bash
gh label list --json name --jq '.[].name' | head -9
```

```bash
gh label create "priority:high" --color B60205 --description "Fix before the next release" --force
gh label create "area:prices" --color 1D76DB --description "prices.txt and price logic" --force
gh label list --json name,description --jq '.[] | select(.name | startswith("priority")) | "\(.name): \(.description)"'
```

```bash
gh issue create --title "Espresso is charged 2.40 instead of 2.50" --body "Found during the evening cash count." \
  --label bug --label "priority:high" --label "area:prices"
```

```bash
gh issue list --label "priority:high" --json number,title,labels \
  --jq '.[] | "#\(.number) \(.title) [\([.labels[].name] | join(", "))]"'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-94
gh issue list --label "good first issue" --json title --jq '.[].title'
```

## Break it

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:hihg" 2>&1
```

## Troubleshoot

```bash
gh label list --json name --jq '.[] | select(.name | startswith("priority")) | .name'
```

## Fix

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:high" > /dev/null
gh issue view "$n" --json labels --jq '[.labels[].name] | join(", ")'
```

## Practice challenge

```bash
cd ~/git-practice/lesson-94
for n in $(gh issue list --state open --json number,title --jq '.[] | select(.title | startswith("Espresso is charged")) | .number'); do
  gh issue close "$n" --reason completed > /dev/null
done
gh label delete "priority:high" --yes && gh label delete "area:prices" --yes
gh label list --json name --jq '.[].name' | grep -c ":" || true
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-94
```
