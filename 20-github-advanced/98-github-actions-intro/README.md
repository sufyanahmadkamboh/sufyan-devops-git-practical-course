# Lesson 98 · GitHub Actions introduction

> Level 20 · GitHub advanced · ⏱ 25 minutes

## What are we learning?

How Git events start automation: a push or a pull request triggers a **workflow** defined in the repository
(`.github/workflows/*.yml`), and GitHub runs it on a fresh machine. This lesson is the bridge from Git to CI/CD: one
small workflow, a failing run, and the fix. GitHub Actions itself (jobs, matrices, secrets, OIDC, deployments) is a
course of its own.

## Visual

```text
 git push ──► GitHub ──► event "push" on main ──► workflow .github/workflows/check.yml
                                                    runs-on: ubuntu-latest
                                                    steps: checkout → check the price file
                                                    ✓ green / ✗ red   (shown on the commit and on PRs)
 branch protection (lesson 59) can REQUIRE the check before merging
```

## Lab setup

<!-- test: github; contains=lesson-98 -->
```bash
bash scripts/new-lab.sh lesson-98 github
cd ~/git-practice/lesson-98
ls
```

<!-- test-run github: gh auth setup-git -->
<!-- test-run github: cd ~/git-practice/lesson-98 && if [ -f .github/workflows/check.yml ]; then git rm -q -r .github && git commit -q -m "test: remove the lesson 98 workflow before re-running the lesson" && git push -q 2> /dev/null; fi -->

## Demonstration

A workflow that checks every line of `prices.csv` (lesson 97 turned prices into CSV) has a name and a number:

<!-- test: github; contains=ci: check the price file -->
```bash
mkdir -p .github/workflows
cat > .github/workflows/check.yml << 'EOF'
name: check-prices
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Every line of prices.csv is "name,price"
        run: |
          bad=$(grep -vE '^[a-z -]+,[0-9]+\.[0-9]{2}$' prices.csv || true)
          if [ -n "$bad" ]; then echo "invalid lines:"; echo "$bad"; exit 1; fi
          echo "prices.csv OK ($(wc -l < prices.csv) items)"
EOF
git add .github/workflows/check.yml
git commit -q -m "ci: check the price file on every push" && git push -q 2> /dev/null
git log --oneline -1
```

The push started a run. Wait for it (GitHub needs a few seconds to register it) and show the result:

<!-- test: github; retry=20; timeout=300; contains=completed; output -->
```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "ci: check the price file on every push")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json status,conclusion,displayTitle --jq '"\(.displayTitle): \(.status), \(.conclusion)"'
```

```text
ci: check the price file on every push: completed, success
```

## Command breakdown

| Command / file | What it does |
|---|---|
| `.github/workflows/NAME.yml` | a workflow: `on:` (events), `jobs:` → `steps:` |
| `gh workflow list` / `gh workflow run NAME` | list / start one manually (with `workflow_dispatch`) |
| `gh run list [--workflow W]` | recent runs |
| `gh run watch ID --exit-status` | follow a run, exit non-zero if it fails |
| `gh run view ID [--log-failed]` | result / logs of the failed steps |
| `gh pr checks` | the checks of a pull request |

## Hands-on exercise

**Instructions.** List the last runs of the workflow with their commit titles and conclusions.

**Expected result.** The run for "ci: check the price file on every push" with `success`.

**Verification.**

<!-- test: github; contains=success -->
```bash
cd ~/git-practice/lesson-98
gh run list --workflow check-prices --limit 3 --json displayTitle,conclusion --jq '.[] | "\(.conclusion) \(.displayTitle)"'
```

## Break it

A careless edit pushed to `main`: a price without decimals.

<!-- test: github; contains=Add flat white -->
```bash
cd ~/git-practice/lesson-98
git pull -q
echo "flat white,3" >> prices.csv && git commit -q -am "Add flat white" && git push -q 2> /dev/null
git log --oneline -1
```

<!-- test: github; retry=20; timeout=300; contains=failure; output -->
```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Add flat white")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json conclusion --jq .conclusion
```

```text
failure
```

## Troubleshoot

The commit shows a red ✗ on GitHub. The failed step's log says exactly what is wrong:

<!-- test: github; retry=20; contains=flat white,3; output -->
```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Add flat white")][0].databaseId')
gh run view "$run" --log-failed | sed -n '/invalid lines:$/,/exit code/p' | sed -E 's/^.*Z //'
```

```text
invalid lines:
flat white,3
##[error]Process completed with exit code 1.
```

## Fix

Fix the data in a new commit; the next run goes green:

<!-- test: github; contains=Fix the flat white price -->
```bash
sed -i 's/^flat white,3$/flat white,3.00/' prices.csv
git commit -q -am "Fix the flat white price" && git push -q 2> /dev/null
git log --oneline -1
```

<!-- test: github; retry=20; timeout=300; contains=success; output -->
```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Fix the flat white price")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json conclusion --jq .conclusion
```

```text
success
```

With branch protection requiring `check-prices` (lesson 59), the broken commit could not have reached `main` at all:
it would have been a red PR instead.

## Real-world example

Every repository in this course series runs its tutorial in CI on each push: the same idea at a larger scale. A
typical DevOps repository has workflows for lint and tests on pull requests, image builds on `main`, releases on `v*`
tags (lesson 97), and deployments with environment approvals, all triggered by Git events you now understand.

## Practice challenge

Add `workflow_dispatch` so the check can be started by hand, start it, and list the run.

<details>
<summary>Solution</summary>

<!-- test: github -->
```bash
cd ~/git-practice/lesson-98
grep -q workflow_dispatch .github/workflows/check.yml || {
  sed -i 's/^  pull_request:$/  pull_request:\n  workflow_dispatch:/' .github/workflows/check.yml
  git commit -q -am "ci: allow manual runs" && git push -q 2> /dev/null
}
sleep 5
gh workflow run check-prices --ref main
```

<!-- test: github; retry=20; contains=workflow_dispatch; output -->
```bash
gh run list --workflow check-prices --limit 1 --json event,status --jq '.[0] | "\(.event) \(.status)"'
```

```text
workflow_dispatch queued
```

</details>

## Recap

- Workflows in `.github/workflows/` run on Git events (push, pull_request, tags, manual).
- `gh run list / watch / view --log-failed` to follow and debug runs.
- Required checks plus branch protection turn CI into a gate for `main`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-98
```

Next: [Module 21 · DevOps workflow](../../21-devops-workflow/README.md).
