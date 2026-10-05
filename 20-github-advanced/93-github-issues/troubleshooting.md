<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 93 · GitHub Issues · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Fix the chai issue on a **feature branch**, with the closing keyword, and push only the branch:

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
git switch -q -c add-chai
echo "chai" >> menu.txt && git commit -q -am "Add chai (closes #$n)"
git push -q -u origin add-chai 2> /dev/null
git log --oneline -1
```

```text
8bf755d (HEAD -> add-chai, origin/add-chai) Add chai (closes #35)
```

```bash
sleep 5
n=$(gh issue list --state all --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --json state --jq .state
```

```text
OPEN
```

## Troubleshoot

Still `OPEN`: closing keywords act only when the commit lands on the **default branch** (`main`). On a feature branch
the commit is linked from the issue's timeline ("referenced this issue"), but the work is not considered done until
it is merged. That is intended: the fix might never be merged.

## Fix

Merge it into `main` (here directly; on a team, by merging the PR):

```bash
git switch -q main && git pull -q && git merge -q --no-edit add-chai && git push -q 2> /dev/null
git push -q origin --delete add-chai 2> /dev/null
```

```bash
n=$(gh issue list --state all --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --json state --jq .state
```

```text
CLOSED
```
