<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 52 · Creating a pull request · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-52 github
cd ~/git-practice/lesson-52
```

## Demonstration

```bash
git switch -q -c add-green-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea to the menu"
git push -u origin add-green-tea 2>&1 | grep -v "^remote: *$"
```

```bash
gh pr create --base main --head add-green-tea \
  --title "Add green tea to the menu" \
  --body "Customers asked for a caffeine-light option. Adds green tea to the menu; the price follows in this PR."
```

```bash
gh pr view add-green-tea --json number,title,state,baseRefName,headRefName,commits \
  --jq '"#\(.number) \(.title) [\(.state)] \(.headRefName) -> \(.baseRefName), \(.commits | length) commit(s)"'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-52
gh pr view add-green-tea --json commits --jq '"\(.commits | length) commit(s)"'
```

## Break it

```bash
gh pr create --base main --head add-green-tea --title "Add green tea" --body "again" 2>&1
```

## Fix

```bash
gh pr edit add-green-tea --title "Green tea: menu and price" > /dev/null
gh pr view add-green-tea --json title --jq .title
```

## Practice challenge

```bash
cd ~/git-practice/lesson-52
git switch -q main && git switch -q -c try-draft
echo "draft idea" > idea.txt && git add idea.txt && git commit -q -m "Draft idea"
git push -q -u origin try-draft 2> /dev/null
gh pr create --draft --base main --title "Draft idea" --body "Work in progress" > /dev/null
gh pr ready try-draft > /dev/null
gh pr view try-draft --json isDraft --jq .isDraft
gh pr close try-draft --delete-branch > /dev/null 2>&1
```

## Cleanup

```bash
cd ~/git-practice/lesson-52
gh pr close add-green-tea --delete-branch > /dev/null 2>&1
```

```bash
cd ~ && rm -rf ~/git-practice/lesson-52
```
