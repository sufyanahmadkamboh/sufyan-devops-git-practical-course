# Lesson 94 · Labels

> Level 20 · GitHub advanced · ⏱ 15 minutes

## What are we learning?

Labels categorise issues and pull requests: type (`bug`, `enhancement`), priority, area (`helm`, `terraform`), status
(`needs-review`). They make lists filterable and drive automation (a `release-notes` label, a CI job that runs only
for `deploy-preview`). We create labels, apply them and filter by them.

## Visual

```text
 #31 Espresso machine shows wrong price   [bug] [priority:high] [area:prices]
 #32 Add chai                             [enhancement] [area:menu]
 #33 Update the Helm chart                [area:helm] [needs-review]

 gh issue list --label "priority:high"  →  #31
```

## Lab setup

<!-- test: github; contains=lesson-94 -->
```bash
bash scripts/new-lab.sh lesson-94 github
cd ~/git-practice/lesson-94
```

## Demonstration

Every new repository has default labels:

<!-- test: github; contains=bug; output -->
```bash
gh label list --json name --jq '.[].name' | head -9
```

```text
accessibility
bug
documentation
duplicate
enhancement
good first issue
help wanted
invalid
question
```

Create the team's own labels (`--force` updates them if they already exist):

<!-- test: github; contains=priority:high; output -->
```bash
gh label create "priority:high" --color B60205 --description "Fix before the next release" --force
gh label create "area:prices" --color 1D76DB --description "prices.txt and price logic" --force
gh label list --json name,description --jq '.[] | select(.name | startswith("priority")) | "\(.name): \(.description)"'
```

```text
priority:high: Fix before the next release
```

Open an issue with labels, and filter:

<!-- test: github; contains=/issues/ -->
```bash
gh issue create --title "Espresso is charged 2.40 instead of 2.50" --body "Found during the evening cash count." \
  --label bug --label "priority:high" --label "area:prices"
```

<!-- test: github; retry=10; contains=Espresso is charged 2.40 instead of 2.50; output -->
```bash
gh issue list --label "priority:high" --json number,title,labels \
  --jq '.[] | "#\(.number) \(.title) [\([.labels[].name] | join(", "))]"'
```

```text
#41 Espresso is charged 2.40 instead of 2.50 [bug, priority:high, area:prices]
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh label list` | labels of the repository |
| `gh label create NAME --color HEX --description D [--force]` | create (or update with `--force`) |
| `gh label edit NAME --name NEW` / `gh label delete NAME --yes` | rename / delete |
| `gh issue edit N --add-label L --remove-label L` | change an issue's labels (also `gh pr edit`) |
| `gh issue list --label L` | filter (several `--label` = all of them) |
| `gh label clone OTHER/REPO` | copy a label set from another repository |

## Hands-on exercise

**Instructions.** Add the label `good first issue` to the espresso issue, and list issues with that label.

**Expected result.** The espresso issue appears.

<!-- test-run github: cd ~/git-practice/lesson-94 && n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number') && gh issue edit "$n" --add-label "good first issue" > /dev/null -->

**Verification.**

<!-- test: github; retry=10; contains=Espresso -->
```bash
cd ~/git-practice/lesson-94
gh issue list --label "good first issue" --json title --jq '.[].title'
```

## Break it

A typo in the label name:

<!-- test: github; fail; contains=not found; output -->
```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:hihg" 2>&1
```

```text
failed to update https://github.com/sufyanahmadkamboh/git-practice-cafe/issues/41: 'priority:hihg' not found
failed to update 1 issue
```

## Troubleshoot

`'priority:hihg' not found`: labels must exist in the repository before they can be applied (the web interface only
offers existing ones; the CLI and API refuse unknown names). Check the exact spelling:

<!-- test: github; contains=priority:high -->
```bash
gh label list --json name --jq '.[] | select(.name | startswith("priority")) | .name'
```

## Fix

<!-- test: github; contains=priority:high; output -->
```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:high" > /dev/null
gh issue view "$n" --json labels --jq '[.labels[].name] | join(", ")'
```

```text
bug, good first issue, priority:high, area:prices
```

## Real-world example

A label scheme kept as code: a `labels.yml` in the repository, synced by a small workflow (or `gh label clone` from a
template repository), so all of a team's repositories share `type:*`, `priority:*`, `area:*` labels. Dashboards then
answer "how many `priority:high` bugs are open across all services?".

## Practice challenge

Close the espresso issue as completed and remove the team labels created here (keep the defaults).

<details>
<summary>Solution</summary>

<!-- test: github; absent=priority:high; output -->
```bash
cd ~/git-practice/lesson-94
for n in $(gh issue list --state open --json number,title --jq '.[] | select(.title | startswith("Espresso is charged")) | .number'); do
  gh issue close "$n" --reason completed > /dev/null
done
gh label delete "priority:high" --yes && gh label delete "area:prices" --yes
gh label list --json name --jq '.[].name' | grep -c ":" || true
```

```text
✓ Closed issue sufyanahmadkamboh/git-practice-cafe#41 (Espresso is charged 2.40 instead of 2.50)
0
```

</details>

## Recap

- Labels categorise issues and PRs by type, priority, area, status.
- `gh label create/list/edit/delete`; apply with `gh issue edit --add-label`.
- Labels must exist before use; share one scheme across repositories.

## Cleanup

<!-- test-run github: cd ~/git-practice/lesson-94 && for n in $(gh issue list --state open --json number,title --jq '.[] | select(.title | startswith("Espresso is charged")) | .number'); do gh issue close "$n" > /dev/null || true; done; gh label delete "priority:high" --yes > /dev/null 2>&1 || true; gh label delete "area:prices" --yes > /dev/null 2>&1 || true -->

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-94
```

Next: [Lesson 95 · Milestones](../95-milestones/README.md).
