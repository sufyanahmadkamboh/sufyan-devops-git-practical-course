# Lesson 95 · Milestones

> Level 20 · GitHub advanced · ⏱ 15 minutes

## What are we learning?

A milestone groups issues and pull requests toward a goal with an optional due date, typically a release
("v1.1.0"). GitHub shows its progress as the share of closed items. We create one, assign issues, close them, and read
the progress.

## Visual

```text
 Milestone v1.1.0   due 2026-12-31            ███████░░░  2 of 3 closed (67 %)
   #40 Add chai                     closed
   #41 Price chai                   closed
   #42 Update the menu board        open
```

## Lab setup

<!-- test: github; contains=lesson-95 -->
```bash
bash scripts/new-lab.sh lesson-95 github
cd ~/git-practice/lesson-95
```

<!-- test-run github: cd ~/git-practice/lesson-95 && me=$(gh api user --jq .login) && for m in $(gh api "repos/$me/git-practice-cafe/milestones?state=all" --jq '.[] | select(.title=="v1.1.0") | .number'); do gh api -X DELETE "repos/$me/git-practice-cafe/milestones/$m" || true; done -->

## Demonstration

The CLI has no milestone command; the API does it (on the web: Issues → Milestones → New milestone):

<!-- test: github; contains=v1.1.0; output -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" -f title="v1.1.0" -f description="Chai and the new menu board" \
  -f due_on="2026-12-31T23:59:59Z" --jq '"\(.title) due \(.due_on[:10]): \(.description)"'
```

```text
v1.1.0 due 2026-12-31: Chai and the new menu board
```

Plan three issues into it:

<!-- test: github -->
```bash
for t in "Add chai" "Price chai" "Update the menu board"; do
  gh issue create --title "$t" --body "Part of v1.1.0." --milestone "v1.1.0" > /dev/null
done
```

<!-- test: github; retry=10; contains=3; output -->
```bash
gh issue list --milestone "v1.1.0" --json title --jq 'length'
```

```text
3
```

Two are done:

<!-- test: github -->
```bash
for t in "Add chai" "Price chai"; do
  n=$(gh issue list --milestone "v1.1.0" --state open --json number,title --jq "[.[] | select(.title == \"$t\")][0].number")
  gh issue close "$n" > /dev/null
done
```

<!-- test: github; retry=10; contains=2 of 3 closed; output -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" --jq '.[] | select(.title=="v1.1.0") | "\(.closed_issues) of \(.open_issues + .closed_issues) closed"'
```

```text
2 of 3 closed
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh api repos/O/R/milestones -f title=T -f due_on=ISO` | create |
| `gh api repos/O/R/milestones --jq …` | list with progress (`open_issues`, `closed_issues`) |
| `gh issue create … --milestone T` / `gh issue edit N --milestone T` | assign |
| `gh issue list --milestone T` | the milestone's issues |
| `gh api -X PATCH repos/O/R/milestones/N -f state=closed` | close the milestone |

## Hands-on exercise

**Instructions.** List the open issues of the milestone.

**Expected result.** Only "Update the menu board".

**Verification.**

<!-- test: github; retry=10; contains=Update the menu board -->
```bash
cd ~/git-practice/lesson-95
gh issue list --milestone "v1.1.0" --state open --json title --jq '.[].title'
```

## Break it

Assign an issue to a milestone that does not exist (the release was renamed):

<!-- test: github; fail; contains=not found; output -->
```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1" 2>&1
```

```text
could not add to milestone 'v1.1': 'v1.1' not found
```

## Troubleshoot

`could not add to milestone 'v1.1': 'v1.1' not found`: milestones are matched by exact title. The issue was not created
(the command failed as a whole). List the existing ones:

<!-- test: github; contains=v1.1.0 -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" --jq '.[].title'
```

## Fix

<!-- test: github; contains=/issues/ -->
```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1.0"
```

## Real-world example

Release planning: issues are assigned to the next version's milestone during planning; the milestone page is the
release's checklist; when it reaches 100 %, the release is tagged (lesson 97) and the milestone closed. Unfinished
items are moved to the next milestone instead of silently slipping.

## Practice challenge

Close all remaining issues of the milestone, then close the milestone itself.

<details>
<summary>Solution</summary>

<!-- test: github; contains=closed; output -->
```bash
cd ~/git-practice/lesson-95
for n in $(gh issue list --milestone "v1.1.0" --state open --json number --jq '.[].number'); do gh issue close "$n" > /dev/null; done
me=$(gh api user --jq .login)
m=$(gh api "repos/$me/git-practice-cafe/milestones" --jq '.[] | select(.title=="v1.1.0") | .number')
gh api -X PATCH "repos/$me/git-practice-cafe/milestones/$m" -f state=closed --jq '"\(.title): \(.state)"'
```

```text
✓ Closed issue sufyanahmadkamboh/git-practice-cafe#39 (Update the menu board)
v1.1.0: closed
```

</details>

## Recap

- A milestone groups issues/PRs toward a goal, usually a release, with progress and a due date.
- Create and inspect with `gh api …/milestones`; assign with `--milestone TITLE`.
- Titles must match exactly.

## Cleanup

<!-- test-run github: cd ~/git-practice/lesson-95 && for n in $(gh issue list --milestone "v1.1.0" --state open --json number --jq '.[].number'); do gh issue close "$n" > /dev/null || true; done -->

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-95
```

Next: [Lesson 96 · Projects](../96-projects/README.md).
