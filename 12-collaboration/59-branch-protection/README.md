# Lesson 59 · Branch protection

> Level 12 · Collaboration · ⏱ 25 minutes

## What are we learning?

How a server enforces the team rules: no direct pushes to `main`, changes only through pull requests, required reviews,
required status checks, no force pushes. First we build the mechanism ourselves with a server-side hook, then we use
GitHub's branch protection on the practice repository.

## Visual

```text
 git push origin main ──► server ──► protection rule for main:
                                       ✗ direct push            → rejected
                                       ✗ force push / deletion  → rejected
                                       ✓ merge of a PR with ≥1 approval and green checks
```

On GitHub: repository → Settings → Branches → "Add branch protection rule" (or Settings → Rules → Rulesets).

## Lab setup

A clone of your GitHub practice repository (lesson 45), for the GitHub part:

<!-- test: github; contains=lesson-59-gh -->
```bash
bash scripts/new-lab.sh lesson-59-gh github
```

<!-- test-run github: gh auth setup-git -->

A local team setup, for building protection ourselves:

<!-- test: contains=lesson-59 -->
```bash
bash scripts/new-lab.sh lesson-59 remote
cd ~/git-practice/lesson-59
```

## Demonstration

**How it works**: the server runs a `pre-receive` hook before accepting a push; if it fails, nothing is updated.
GitHub's protection is the same idea, configured instead of scripted. A minimal rule for our server:

<!-- test: contains=pre-receive -->
```bash
cat > server/cafe.git/hooks/pre-receive << 'EOF'
#!/usr/bin/env bash
# reject direct updates of main; changes arrive through merged pull requests (here: only the "pr-bot" may push main)
while read -r old new ref; do
  if [ "$ref" = "refs/heads/main" ] && [ "${PUSHER:-}" != "pr-bot" ]; then
    echo "error: main is protected: changes must be made through a pull request"
    exit 1
  fi
done
EOF
chmod +x server/cafe.git/hooks/pre-receive
ls server/cafe.git/hooks/ | grep -v sample
```

Ada pushes to `main` directly:

<!-- test: fail; contains=main is protected; output -->
```bash
cd ada && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push 2>&1
```

```text
remote: error: main is protected: changes must be made through a pull request        
To ~/git-practice/lesson-59/server/cafe.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to '~/git-practice/lesson-59/server/cafe.git'
```

Branches are allowed; the "merge" is done by the PR system (`PUSHER=pr-bot`):

<!-- test: contains=main -> main; output -->
```bash
git push -q origin HEAD:refs/heads/add-chai 2>&1
git reset -q --hard origin/main
cd ../grace && git fetch -q && git merge -q --ff-only origin/add-chai
PUSHER=pr-bot git push 2>&1
```

```text
To ~/git-practice/lesson-59/server/cafe.git
   4267004..1c6033f  main -> main
```

## Command breakdown

| GitHub protection setting | Effect |
|---|---|
| Require a pull request before merging | no direct pushes to the branch |
| Required approvals: 1 | someone other than the author must approve (lesson 53) |
| Require status checks to pass | CI must be green (lesson 98) |
| Require branches to be up to date | the PR must contain the latest `main` |
| Do not allow bypassing (enforce for admins) | the rules apply to administrators too |
| Allow force pushes / deletions: off | history of `main` cannot be rewritten or deleted |

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

<!-- test: github; contains=approvals: 1, enforce_admins: true -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches/main/protection" \
  --jq '"approvals: \(.required_pull_request_reviews.required_approving_review_count), enforce_admins: \(.enforce_admins.enabled)"'
```

## Break it

Push directly to the protected `main` on GitHub, even as the repository's owner:

<!-- test: github; fail; contains=Protected branch update failed; output -->
```bash
cd ~/git-practice/lesson-59-gh
echo "chai" >> menu.txt && git commit -q -am "Add chai directly"
git push 2>&1 | grep -E "remote: (error|-)|rejected|GH006" | head -4
test "${PIPESTATUS[0]}" -eq 0
```

```text
remote: error: GH006: Protected branch update failed for refs/heads/main.        
remote: - Changes must be made through a pull request.        
 ! [remote rejected] main -> main (protected branch hook declined)
```

## Troubleshoot

`GH006: Protected branch update failed for refs/heads/main` and `Changes must be made through a pull request`: the
rule works, including for the owner (enforced for admins). Nothing changed on GitHub; the commit is only local.

## Fix

The commit belongs on a branch with a PR:

<!-- test: github; contains=/pull/; output -->
```bash
git switch -q -c add-chai-direct
git push -q -u origin add-chai-direct 2>&1 | grep -v "^remote:" || true
gh pr create --base main --title "Add chai" --body "Through a PR, as main is protected."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/13
```

The PR now needs one approval from someone else before it can be merged (on a solo practice repository, nobody can:
the rule is doing its job).

## Real-world example

A typical production setup: `main` protected with 1–2 required approvals, required CI checks (`build`, `test`,
`helm-lint`), "require branches to be up to date", "require conversation resolution", **CODEOWNERS** (a file assigning
reviewers per path, e.g. `/helm/ @platform-team`), no bypass. Release tags can be protected by tag rulesets as well.

## Practice challenge

List which of your practice repository's branches are protected.

<details>
<summary>Solution</summary>

<!-- test: github; contains=main; output -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches?protected=true" --jq '.[].name'
```

```text
main
```

</details>

## Recap

- Protection is enforced by the server at push time (GitHub rules ≈ a managed `pre-receive` hook).
- Require PRs, approvals and checks; disallow force pushes; enforce for admins.
- A rejected push changes nothing on the server: move the commit to a branch and open a PR.

## Cleanup

Remove the protection and the PR, so later lessons can merge into the practice repository freely:

<!-- test: github -->
```bash
cd ~/git-practice/lesson-59-gh
me=$(gh api user --jq .login)
gh pr close add-chai-direct --delete-branch > /dev/null 2>&1 || true
gh api -X DELETE "repos/$me/git-practice-cafe/branches/main/protection"
```

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-59 ~/git-practice/lesson-59-gh
```

Next: [Module 13 · Lesson 60 · What is rebase?](../../13-rebase/60-what-is-rebase/README.md).
