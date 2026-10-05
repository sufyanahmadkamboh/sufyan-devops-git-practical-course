# Lesson 52 · Creating a pull request

> Level 11 · Pull requests · ⏱ 20 minutes

## What are we learning?

The full loop on the real GitHub: branch, commit, push, open a PR with a useful title and description, update it with
more commits. We use the GitHub CLI; the web flow is shown alongside.

## Visual

```text
 git switch -c add-green-tea → commit → git push -u origin add-green-tea
        │
        ▼  GitHub shows a yellow banner: "add-green-tea had recent pushes [Compare & pull request]"
 gh pr create --base main --title "..." --body "..."
        │
        ▼
 PR #N open ── new commits pushed to add-green-tea appear in the PR automatically
```

## Lab setup

<!-- test: github; contains=lesson-52 -->
```bash
bash scripts/new-lab.sh lesson-52 github
cd ~/git-practice/lesson-52
```

<!-- test-run github: gh auth setup-git -->
<!-- test-run github: cd ~/git-practice/lesson-52 && (git push -q origin --delete add-green-tea 2> /dev/null || true) -->

## Demonstration

<!-- test: github; contains=add-green-tea; output -->
```bash
git switch -q -c add-green-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea to the menu"
git push -u origin add-green-tea 2>&1 | grep -v "^remote: *$"
```

```text
remote: Create a pull request for 'add-green-tea' on GitHub by visiting:        
remote:      https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/new/add-green-tea        
To https://github.com/sufyanahmadkamboh/git-practice-cafe.git
 * [new branch]      add-green-tea -> add-green-tea
branch 'add-green-tea' set up to track 'origin/add-green-tea'.
```

GitHub even prints the link to create the PR. With the CLI:

<!-- test: github; contains=/pull/; output -->
```bash
gh pr create --base main --head add-green-tea \
  --title "Add green tea to the menu" \
  --body "Customers asked for a caffeine-light option. Adds green tea to the menu; the price follows in this PR."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/8
```

<!-- test: github; contains=OPEN; output -->
```bash
gh pr view add-green-tea --json number,title,state,baseRefName,headRefName,commits \
  --jq '"#\(.number) \(.title) [\(.state)] \(.headRefName) -> \(.baseRefName), \(.commits | length) commit(s)"'
```

```text
#8 Add green tea to the menu [OPEN] add-green-tea -> main, 1 commit(s)
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh pr create --base B --title T --body X` | open a PR from the current branch into B |
| `gh pr create --fill` | title/body from the commit messages |
| `gh pr create --draft` | a draft: visible, not ready for review or merging |
| `gh pr view [N|BRANCH] [--web]` | details (or open the page) |
| `gh pr diff` / `gh pr checks` | the diff / the CI status |
| `gh pr edit --add-reviewer X --add-label Y` | change reviewers, labels, title, body |
| `gh pr close N --delete-branch` | close without merging |

## Hands-on exercise

**Instructions.** Push a second commit (the price) to the branch, and check that the PR now has two commits.

**Expected result.** `2 commit(s)`.

<!-- test-run github: cd ~/git-practice/lesson-52 && echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea" && git push -q 2> /dev/null -->

**Verification.**

<!-- test: github; retry=10; contains=2 commit(s) -->
```bash
cd ~/git-practice/lesson-52
gh pr view add-green-tea --json commits --jq '"\(.commits | length) commit(s)"'
```

## Break it

Run `gh pr create` again for the same branch:

<!-- test: github; fail; contains=already exists; output -->
```bash
gh pr create --base main --head add-green-tea --title "Add green tea" --body "again" 2>&1
```

```text
a pull request for branch "add-green-tea" into branch "main" already exists:
https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/8
```

## Troubleshoot

A branch can have only one open PR into the same base. The second one is unnecessary: pushing to the branch already
updated the existing PR. If the title or description needs to change, edit the PR instead of opening a new one.

## Fix

<!-- test: github; contains=Green tea: menu and price; output -->
```bash
gh pr edit add-green-tea --title "Green tea: menu and price" > /dev/null
gh pr view add-green-tea --json title --jq .title
```

```text
Green tea: menu and price
```

## Real-world example

A good PR description answers: **why** (the problem, a link to the issue), **what** (the change in two lines), **how
it was tested** (commands, screenshots), **risks** (migration, config change, rollback). Many repositories put a
template in `.github/pull_request_template.md` so every new PR starts with these headings.

## Practice challenge

Open a **draft** PR from a new branch, then mark it ready for review, and close it (with its branch) to keep the
practice repository tidy.

<details>
<summary>Solution</summary>

<!-- test: github; contains=false; output -->
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

```text
✓ Pull request sufyanahmadkamboh/git-practice-cafe#9 is marked as "ready for review"
false
```

</details>

## Recap

- Push the branch, then `gh pr create` (or the "Compare & pull request" button).
- New commits on the branch update the PR; one open PR per branch and base.
- Write the why, what, how-tested in the description; drafts for early feedback.

## Cleanup

Close the PR and delete its branch (lesson 53 creates its own):

<!-- test: github -->
```bash
cd ~/git-practice/lesson-52
gh pr close add-green-tea --delete-branch > /dev/null 2>&1
```

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-52
```

Next: [Lesson 53 · Pull request review](../53-pull-request-review/README.md).
