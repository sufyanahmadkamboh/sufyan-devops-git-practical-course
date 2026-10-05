# Lesson 57 · GitHub Flow

> Level 12 · Collaboration · ⏱ 20 minutes

## What are we learning?

GitHub Flow is the simplest common team workflow: `main` is always deployable; every change goes through a short branch
and a pull request; what is merged is deployed. We run it end to end with a tiny "deployment".

## Visual

```text
 main (always deployable) ──●──────────●──────────●───►  deploy on every merge
                             ╲        ╱ ╲        ╱
                              branch ─PR  branch─PR
                              1. branch  2. commits  3. PR + review + checks  4. merge  5. deploy  6. delete branch
```

## Lab setup

The "production" is a folder that always contains what `main` on the server contains:

<!-- test: contains=lesson-57 -->
```bash
bash scripts/new-lab.sh lesson-57 remote
cd ~/git-practice/lesson-57
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh: put the server's main into production/, and run the smoke test
set -e
rm -rf production && git clone -q server/cafe.git production
grep -q "^espresso [0-9]" production/prices.txt && echo "deployed $(git -C production log --oneline -1)"
EOF
bash deploy.sh
```

## Demonstration

One change, the GitHub Flow way. Branch and commit:

<!-- test: contains=menu.txt -->
```bash
cd ada
git switch -q -c add-chai
echo "chai" >> menu.txt && echo "chai 3.10" >> prices.txt && git commit -q -am "Add chai"
git push -q -u origin add-chai
git diff --stat main...add-chai
```

Review and checks (here: the smoke test against the branch), then merge into `main` (the PR's merge button) and deploy:

<!-- test: contains=deployed; contains=Merge branch 'add-chai'; output -->
```bash
grep -q "^espresso [0-9]" prices.txt && echo "check passed"
git switch -q main && git merge -q --no-ff --no-edit add-chai && git push -q
git push -q origin --delete add-chai && git branch -d add-chai
cd .. && bash deploy.sh
```

```text
check passed
Deleted branch add-chai (was 3742ae9).
deployed fdb306b (HEAD -> main, origin/main, origin/HEAD) Merge branch 'add-chai'
```

## Command breakdown

| Rule of GitHub Flow | In practice |
|---|---|
| `main` is always deployable | protect it (lesson 59); CI on every PR |
| branch from `main`, descriptive names | `git switch -c add-chai` |
| open a PR early | draft PRs for discussion (lesson 52) |
| merge only after review and green checks | branch protection rules |
| deploy right after merging | CD triggered by pushes to `main` (lesson 98) |

## Hands-on exercise

**Instructions.** Ship one more change through the flow: Grace adds `mocha` on a branch, merges, deploys.

**Expected result.** Production shows `Add mocha`.

<!-- test-run: cd ~/git-practice/lesson-57/grace && git pull -q && git switch -q -c add-mocha && echo mocha >> menu.txt && git commit -q -am "Add mocha" && git switch -q main && git merge -q --no-ff -m "Merge branch 'add-mocha'" add-mocha && git push -q -->

**Verification.**

<!-- test: contains=add-mocha -->
```bash
cd ~/git-practice/lesson-57
bash deploy.sh
```

## Break it

Skip the flow: a "quick fix" pushed straight to `main`, without review or checks, breaks the prices file.

<!-- test: fail; output -->
```bash
cd ~/git-practice/lesson-57/ada && git pull -q
sed -i 's/^espresso 2.50/espresso two-fifty/' prices.txt && git commit -q -am "Quick fix" && git push -q
cd .. && bash deploy.sh
```

```text
```

## Troubleshoot

Production's smoke test failed (`deploy.sh` stopped with exit status 1 and printed no `deployed` line): `main` is no
longer deployable, and every later merge is blocked behind it. Find the culprit:

<!-- test: contains=Quick fix; output -->
```bash
git -C server/cafe.git log --oneline -3
git -C ada show --format=%s HEAD -- prices.txt | grep -E "^[-+]espresso|Quick"
```

```text
b407c2d (HEAD -> main) Quick fix
e2958c4 Merge branch 'add-mocha'
e9ae25b Add mocha
Quick fix
-espresso 2.50
+espresso two-fifty
```

## Fix

The fastest safe fix on a shared `main`: revert it, **through the same flow** (branch, check, merge), and deploy:

<!-- test: contains=deployed; output -->
```bash
cd ada
git switch -q -c revert-quick-fix && git revert --no-edit HEAD > /dev/null
grep -q "^espresso [0-9]" prices.txt && echo "check passed"
git switch -q main && git merge -q --no-ff --no-edit revert-quick-fix && git push -q
cd .. && bash deploy.sh
```

```text
check passed
deployed 333283f (HEAD -> main, origin/main, origin/HEAD) Merge branch 'revert-quick-fix'
```

## Real-world example

GitHub Flow with CD is the default for web services: merging the PR triggers a pipeline that builds the image, pushes
it to a registry and deploys it (lesson 98, and the CI/CD course). Rollbacks are reverts (or redeploying the previous
image), done through the same PR process, so `main` and production never disagree for long.

## Practice challenge

Turn the smoke test into a guard: make `deploy.sh` refuse to replace production when the new version fails, keeping the
previous one running.

<details>
<summary>Solution</summary>

<!-- test: contains=kept; output -->
```bash
cd ~/git-practice/lesson-57
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh: test the server's main in a staging folder, and only then replace production/
set -e
rm -rf staging && git clone -q server/cafe.git staging
if grep -q "^espresso [0-9]" staging/prices.txt; then
  rm -rf production && mv staging production && echo "deployed $(git -C production log --oneline -1)"
else
  echo "smoke test failed: kept $(git -C production log --oneline -1)"; exit 1
fi
EOF
(cd ada && sed -i 's/^espresso 2.50/espresso broken/' prices.txt && git commit -q -am "Another quick fix" && git push -q)
bash deploy.sh || true
```

```text
smoke test failed: kept 333283f (HEAD -> main, origin/main, origin/HEAD) Merge branch 'revert-quick-fix'
```

</details>

## Recap

- GitHub Flow: `main` always deployable; branch → PR → review/checks → merge → deploy.
- Bypassing review and checks breaks production for everyone.
- Fix forward through the same flow: a revert PR.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-57
```

Next: [Lesson 58 · Git Flow](../58-git-flow/README.md).
