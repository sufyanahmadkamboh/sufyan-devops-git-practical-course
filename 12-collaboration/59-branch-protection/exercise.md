<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 59 · Branch protection · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Protect `main` of your GitHub practice repository: pull requests required with one approval, enforced
for administrators.

**Expected result.** `approvals: 1, enforce_admins: true`.

<!-- test-run github: cd ~/git-practice/lesson-59-gh && me=$(gh api user --jq .login) && printf '{"required_status_checks":null,"enforce_admins":true,"required_pull_request_reviews":{"required_approving_review_count":1},"restrictions":null,"allow_force_pushes":false,"allow_deletions":false}' | gh api -X PUT "repos/$me/git-practice-cafe/branches/main/protection" --input - > /dev/null -->

The command (the JSON body is what the Settings page sends):

```bash
me=$(gh api user --jq .login)
printf '{"required_status_checks":null,"enforce_admins":true,"required_pull_request_reviews":{"required_approving_review_count":1},"restrictions":null,"allow_force_pushes":false,"allow_deletions":false}' |
  gh api -X PUT "repos/$me/git-practice-cafe/branches/main/protection" --input -
```

**Verification.**

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches/main/protection" \
  --jq '"approvals: \(.required_pull_request_reviews.required_approving_review_count), enforce_admins: \(.enforce_admins.enabled)"'
```
