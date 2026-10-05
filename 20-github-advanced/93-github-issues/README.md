# Lesson 93 · GitHub Issues

> Level 20 · GitHub advanced · ⏱ 20 minutes

## What are we learning?

Issues track work: bugs, feature requests, tasks. The useful part for Git users is the link between issues and
commits: writing `Fixes #12` in a commit or PR closes the issue automatically when the change reaches the default
branch. We run that workflow on the practice repository.

## Visual

```text
 Issue #N "Green tea has no price"  (open)
        │  assigned, labelled (lesson 94), in a milestone (lesson 95)
        ▼
 branch fix-green-tea-price → commit "Price green tea (fixes #N)" → PR → merge into main
        │
        ▼
 Issue #N closed automatically, with a link to the commit / PR
 closing keywords: close(s/d), fix(es/ed), resolve(s/d) + #N   (only on the DEFAULT branch)
```

## Lab setup

<!-- test: github; contains=lesson-93 -->
```bash
bash scripts/new-lab.sh lesson-93 github
cd ~/git-practice/lesson-93
```

<!-- test-run github: gh auth setup-git -->
<!-- test-run github: cd ~/git-practice/lesson-93 && if [ -f prices.csv ]; then git rm -q prices.csv && git show 4267004:prices.txt > prices.txt && git add prices.txt && git commit -q -m "test: restore prices.txt for the lessons" && git push -q 2> /dev/null; fi; sed -i '/^green tea /d' prices.txt; git diff --quiet || { git commit -q -am "test: remove the green tea price for lesson 93" && git push -q 2> /dev/null; } -->

`gh issue list` shows the newest issues first; the lesson finds its issues by exact title with `--jq`.

## Demonstration

Report the bug:

<!-- test: github; contains=/issues/; output -->
```bash
gh issue create --title "Green tea has no price" \
  --body "Green tea is on the menu, but prices.txt has no line for it. Customers cannot order it."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/issues/34
```

<!-- test: github; contains=Green tea has no price; output -->
```bash
gh issue list --state open --json number,title,state \
  --jq '.[] | select(.title == "Green tea has no price") | "#\(.number) \(.title) [\(.state)]"'
```

```text
#34 Green tea has no price [OPEN]
```

Fix it with a commit that references the issue, and push to `main` (on a team: through a PR whose description says
`Fixes #N`):

<!-- test: github; contains=main -> main; output -->
```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Green tea has no price")][0].number')
echo "green tea 2.80" >> prices.txt
git commit -q -am "Price green tea (fixes #$n)"
git push 2>&1 | tail -1
```

```text
   10c8592..ea774fb  main -> main
```

GitHub closes the issue and links the commit (it can take a few seconds):

<!-- test: github; retry=10; contains=CLOSED; output -->
```bash
gh issue list --state all --json number,title,state \
  --jq '[.[] | select(.title == "Green tea has no price")][0] | "#\(.number) \(.state)"'
```

```text
#34 CLOSED
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh issue create --title T --body B [--label L --assignee @me]` | open an issue |
| `gh issue list [--state all] [--label L] [--search Q]` | list / filter (`--search` uses GitHub search, which can lag a little) |
| `gh issue view N [--comments]` | details |
| `gh issue comment N --body B` | comment |
| `gh issue close N [--reason "not planned"]` / `reopen` | close / reopen by hand |
| `Fixes #N` in a commit or PR description | close N when merged into the default branch |

## Hands-on exercise

**Instructions.** Open a second issue, "Add chai to the menu", comment on it, and view it with its comments.

**Expected result.** The issue with your comment.

<!-- test-run github: cd ~/git-practice/lesson-93 && gh issue create --title "Add chai to the menu" --body "Several customers asked for chai." > /dev/null && n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number') && gh issue comment "$n" --body "I will take this one." > /dev/null -->

**Verification.**

<!-- test: github; contains=I will take this one -->
```bash
cd ~/git-practice/lesson-93
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --comments | tail -4
```

## Break it

Fix the chai issue on a **feature branch**, with the closing keyword, and push only the branch:

<!-- test: github; output -->
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

<!-- test: github; contains=OPEN; output -->
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

<!-- test: github -->
```bash
git switch -q main && git pull -q && git merge -q --no-edit add-chai && git push -q 2> /dev/null
git push -q origin --delete add-chai 2> /dev/null
```

<!-- test: github; retry=10; contains=CLOSED; output -->
```bash
n=$(gh issue list --state all --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --json state --jq .state
```

```text
CLOSED
```

## Real-world example

Teams use issue **templates** (`.github/ISSUE_TEMPLATE/bug.yml`) so bug reports always include version, steps,
expected and actual behaviour; PR descriptions say `Closes #123`; release notes are generated from the merged PRs and
the issues they closed. An issue number in every branch name (`fix/123-green-tea-price`) makes the trail complete.

## Practice challenge

Show the newest closed issue with each of the two titles, and how it was closed (`closedByPullRequestsReferences`
is empty here because the fixes were commits, not PRs).

<details>
<summary>Solution</summary>

<!-- test: github; contains=Add chai to the menu; output -->
```bash
cd ~/git-practice/lesson-93
gh issue list --state closed --limit 50 --json number,title,stateReason \
  --jq '[.[] | select(.title == "Green tea has no price" or .title == "Add chai to the menu")] | unique_by(.title)[] | "#\(.number) \(.title): \(.stateReason)"'
```

```text
#35 Add chai to the menu: COMPLETED
#34 Green tea has no price: COMPLETED
```

</details>

## Recap

- Issues track work; `gh issue create/list/view/comment/close`.
- `Fixes #N` / `Closes #N` in a commit or PR closes the issue when it reaches the default branch.
- On other branches the commit is only referenced; merging closes it.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-93
```

Next: [Lesson 94 · Labels](../94-labels/README.md).
