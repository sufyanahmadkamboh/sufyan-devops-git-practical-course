<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 53 · Pull request review · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Approve your own PR:

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

```bash
gh pr review price-green-tea --approve --body "Price with tax confirmed. Thanks!"
```

On a solo practice repository there is no second person: the lesson stops here, and the next steps (merging) work
because the practice repository has no protection rule requiring approvals.
