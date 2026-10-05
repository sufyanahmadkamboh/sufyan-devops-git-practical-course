# Lesson 53 · Pull request review

> Level 11 · Pull requests · ⏱ 25 minutes

## What are we learning?

How a review works on GitHub: general comments, comments on a line, **suggestions** the author can apply with one
click, and the three review verdicts (comment, approve, request changes). And why you cannot approve your own PR.

## Visual

```text
 PR #N  ── Files changed ── line 4 of prices.txt
              │
              ├── comment            "Is 2.80 the price with tax?"
              ├── suggestion         ```suggestion
              │                      green tea 2.90
              │                      ```                    → author clicks "Commit suggestion"
              └── conversation       replies … → "Resolve conversation"

 Submit review:  ○ Comment   ○ Approve   ○ Request changes
                  (no verdict)  (ready)    (blocks merging while protection requires reviews)
```

## Lab setup

The author (you) opens a PR to review:

<!-- test: github; contains=lesson-53 -->
```bash
bash scripts/new-lab.sh lesson-53 github
cd ~/git-practice/lesson-53
```

<!-- test-run github: gh auth setup-git -->
<!-- test-run github: cd ~/git-practice/lesson-53 && (git push -q origin --delete price-green-tea 2> /dev/null || true) -->

<!-- test: github; contains=/pull/ -->
```bash
git switch -q -c price-green-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git push -q -u origin price-green-tea 2> /dev/null
gh pr create --base main --title "Price green tea" --body "Adds the green tea price."
```

## Demonstration

A general review comment (verdict "Comment"):

<!-- test: github; output -->
```bash
gh pr review price-green-tea --comment --body "Looks good overall. One question on the price, see the line comment."
gh pr view price-green-tea --json reviews --jq '.reviews[] | "\(.state): \(.body)"'
```

```text
COMMENTED: Looks good overall. One question on the price, see the line comment.
```

A comment on a specific line, containing a **suggestion**. The CLI has no command for line comments, so we use the API
(on the web: hover the line in "Files changed", click `+`):

<!-- test: github; contains=suggestion; output -->
```bash
me=$(gh api user --jq .login)
number=$(gh pr view price-green-tea --json number --jq .number)
commit=$(git rev-parse HEAD)
body=$(printf 'Our prices include tax: 2.80 is the price before tax.\n```suggestion\ngreen tea 2.90\n```')
gh api "repos/$me/git-practice-cafe/pulls/$number/comments" \
  -f body="$body" -f commit_id="$commit" -f path=prices.txt -F line=4 -f side=RIGHT --jq '"\(.path):\(.line) \(.body)"'
```

```text
prices.txt:4 Our prices include tax: 2.80 is the price before tax.
```suggestion
green tea 2.90
```
```suggestion
green tea 2.90
```
```suggestion
green tea 2.90
```
```

The author applies the suggestion (on the web: "Commit suggestion"; here, the same change as a commit):

<!-- test: github -->
```bash
sed -i 's/^green tea 2.80$/green tea 2.90/' prices.txt
git commit -q -am "Price green tea with tax" && git push -q 2> /dev/null
```

The PR shows the new version (GitHub may need a few seconds after the push):

<!-- test: github; retry=10; contains=green tea 2.90; output -->
```bash
gh pr diff price-green-tea
```

```text
diff --git a/prices.txt b/prices.txt
index 864a958..590362e 100644
--- a/prices.txt
+++ b/prices.txt
@@ -2,3 +2,4 @@ espresso 2.50
 latte 3.20
 cappuccino 3.40
 chai 3.10
+green tea 2.90
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh pr review N --comment -b TEXT` | review without a verdict |
| `gh pr review N --approve [-b TEXT]` | approve |
| `gh pr review N --request-changes -b TEXT` | request changes |
| `gh pr comment N -b TEXT` | a conversation comment (not a review) |
| `gh api repos/O/R/pulls/N/comments -f path=… -F line=…` | a line comment (with an optional ```suggestion block) |
| `gh pr checkout N` | check the PR's branch out locally to test it |

## Hands-on exercise

**Instructions.** List every line comment of the PR with its file and line.

**Expected result.** `prices.txt:4 …`.

**Verification.**

<!-- test: github; contains=prices.txt -->
```bash
me=$(gh api user --jq .login)
number=$(gh pr view price-green-tea --json number --jq .number)
gh api "repos/$me/git-practice-cafe/pulls/$number/comments" --jq '.[] | "\(.path):\(.original_line) \(.user.login)"'
```

## Break it

Approve your own PR:

<!-- test: github; fail; contains=Can not approve your own pull request; output -->
```bash
gh pr review price-green-tea --approve 2>&1
```

```text
failed to create review: GraphQL: Review Can not approve your own pull request (addPullRequestReview)
```

## Troubleshoot

`Can not approve your own pull request`: a review is a second person's check. GitHub does not count the author, and
"request changes" on your own PR is refused for the same reason. If a repository requires one approval (lesson 59), a
PR cannot be merged until someone else with write access approves it.

## Fix

Ask a reviewer (`gh pr edit price-green-tea --add-reviewer TEAMMATE`, or "Reviewers" on the PR page). The reviewer,
logged in as themselves, runs:

<!-- test: skip -->
```bash
gh pr review price-green-tea --approve --body "Price with tax confirmed. Thanks!"
```

On a solo practice repository there is no second person: the lesson stops here, and the next steps (merging) work
because the practice repository has no protection rule requiring approvals.

## Real-world example

Good reviews: ask questions instead of giving orders ("What happens if the value is empty?"), separate blocking
issues from nits ("nit: typo"), use suggestions for small fixes, approve when it is good enough rather than perfect.
In infrastructure repositories, reviewers check the **plan** output (Terraform), the rendered manifests (`helm
template`), and the rollback path, not only the diff.

## Practice challenge

Add a conversation comment (not a review) linking to the review guidelines, then count all comments on the PR.

<details>
<summary>Solution</summary>

<!-- test: github; output -->
```bash
cd ~/git-practice/lesson-53
gh pr comment price-green-tea --body "Reviewed following docs/review-guidelines.md" > /dev/null
gh pr view price-green-tea --json comments,reviews --jq '"comments: \(.comments | length), reviews: \(.reviews | length)"'
```

```text
comments: 1, reviews: 2
```

</details>

## Recap

- Review verdicts: comment, approve, request changes; line comments can carry one-click suggestions.
- The author answers by pushing commits; the PR updates.
- Nobody can approve their own PR: required reviews need a second person.

## Cleanup

<!-- test: github -->
```bash
cd ~/git-practice/lesson-53
gh pr close price-green-tea --delete-branch > /dev/null 2>&1
```

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-53
```

Next: [Lesson 54 · Merge strategies](../54-merge-strategies/README.md).
