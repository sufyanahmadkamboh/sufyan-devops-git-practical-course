# Module 12 · Collaboration · Assessment

> Lessons 55–59 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

A team repository for the practical challenge, and a Git Flow repository with a mistake in it:

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-12-team remote
bash scripts/new-lab.sh assess-12-flow basic
(cd ~/git-practice/assess-12-flow &&
  git tag -a v1.0.0 -m "Release 1.0.0" && git switch -q -c develop &&
  echo "green tea" >> menu.txt && git commit -q -am "Add green tea" &&
  git switch -q -c hotfix/1.0.1 main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Fix the espresso price" &&
  git switch -q main && git merge -q --no-ff --no-edit hotfix/1.0.1 && git tag -a v1.0.1 -m "Release 1.0.1" &&
  git branch -q -d hotfix/1.0.1 && git switch -q develop)
```

## Quiz

1. Two developers commit directly on `main` and push minutes apart. What does the second one see, and what should
   they run?
2. Name three habits of the feature branch workflow that keep conflicts small.
3. In GitHub Flow, what must always be true of `main`?
4. In Git Flow, which branches does a `hotfix/*` branch start from and merge into?
5. When is Git Flow a good fit, and when does it add unnecessary complexity?
6. What does a server-side `pre-receive` hook have in common with GitHub branch protection?
7. Which branch protection setting makes the rules apply to repository administrators too?
8. Why is "Require status checks to pass" more reliable than asking developers to run tests locally?

<details>
<summary>Answers</summary>

1. `! [rejected] main -> main (fetch first)`; integrate first (`git pull --rebase`), then push (lesson 55).
2. Start from the latest `main`, keep branches short-lived, merge `main` into the branch regularly (56).
3. It is always deployable: everything merged is reviewed, checked and ready to deploy (57).
4. From `main`; merged into `main` **and** `develop` (58).
5. Good for versioned products with several supported releases; heavy for continuously deployed services (58).
6. Both run on the server at push time and reject updates that break the rules (59).
7. "Do not allow bypassing" / enforce for admins (59).
8. The server enforces it for every PR, on a clean machine; local checks can be skipped or differ (57, 59).

</details>

## Practical challenge

In `~/git-practice/assess-12-team`, set up and use a protected `main`.

Requirements:

1. The server rejects direct pushes to `main` unless the pusher is the PR bot (`PUSHER=pr-bot`).
2. Ada develops `feature/chai` on a branch and pushes it.
3. Grace reviews it and merges it as the PR bot with a merge commit; the branch is deleted on the server.

<details>
<summary>Reference solution</summary>

<!-- test: contains=main -> main; output -->
```bash
cd ~/git-practice/assess-12-team
cat > server/cafe.git/hooks/pre-receive << 'EOF'
#!/usr/bin/env bash
while read -r old new ref; do
  if [ "$ref" = refs/heads/main ] && [ "${PUSHER:-}" != pr-bot ]; then
    echo "error: main is protected: open a pull request"; exit 1
  fi
done
EOF
chmod +x server/cafe.git/hooks/pre-receive
(cd ada && git switch -q -c feature/chai && echo "chai" >> menu.txt && git commit -q -am "feat(menu): add chai" && git push -q -u origin feature/chai)
cd grace && git fetch -q
git log --oneline main..origin/feature/chai
git merge -q --no-ff -m "Merge pull request from feature/chai" origin/feature/chai
PUSHER=pr-bot git push 2>&1 | tail -1
git push -q origin --delete feature/chai
```

```text
7ec0de9 (origin/feature/chai) feat(menu): add chai
   4267004..d924be9  main -> main
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-12-team/ada && git switch -q main && git pull -q
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "direct push to main is rejected" '! (git commit -q --allow-empty -m "direct" && git push -q origin main); git reset -q --hard origin/main'
check "chai merged with a merge commit" 'git log --merges --format=%s origin/main | grep -q feature/chai && grep -q chai menu.txt'
check "feature branch deleted on the server" '[ -z "$(git ls-remote --heads origin feature/chai)" ]'
```

```text
ok       direct push to main is rejected
ok       chai merged with a merge commit
ok       feature branch deleted on the server
```

## Troubleshooting challenge

In `~/git-practice/assess-12-flow` (Git Flow), release 1.0.1 fixed the espresso price on `main`. QA reports that the
next release candidate, built from `develop`, charges the old price again.

Symptoms:

<!-- test: contains=espresso 2.50; output -->
```bash
cd ~/git-practice/assess-12-flow
git show main:prices.txt | head -1
git show develop:prices.txt | head -1
```

```text
espresso 2.60
espresso 2.50
```

Find the cause and fix it so the next release keeps the fix.

<details>
<summary>Solution</summary>

`main` has a commit `develop` does not: the hotfix was merged into `main` only (lesson 58).

<!-- test: contains=Fix the espresso price; output -->
```bash
git log --oneline develop..main
```

```text
4d2287d (tag: v1.0.1, main) Merge branch 'hotfix/1.0.1'
edd3a38 Fix the espresso price
```

<!-- test: contains=espresso 2.60; output -->
```bash
git switch -q develop
git merge -q --no-edit main
head -1 prices.txt
```

```text
espresso 2.60
```

</details>

Verification: nothing on `main` is missing from `develop`, and green tea is still there.

<!-- test: contains=0; output -->
```bash
cd ~/git-practice/assess-12-flow
git log --oneline develop..main | wc -l
grep -c "green tea" menu.txt
```

```text
0
1
```

## Real-world scenario

Your team of six pushes directly to `main` "to save time". Last week a broken commit reached production twice. The lead
asks you to propose a workflow that does not slow everyone down.

<details>
<summary>Model answer</summary>

Propose GitHub Flow: short branches, small PRs, one approval, required CI checks, automatic deploy after merge.
Enforce it with branch protection on `main` (PR required, required status checks, no force pushes, enforced for
admins). Keep it fast: CI under ten minutes, a PR template, auto-delete merged branches, review rotation so PRs wait
hours, not days. Roll back with revert PRs. Avoid Git Flow here: the team deploys continuously, so `develop` and release
branches would only add delay.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-12-team ~/git-practice/assess-12-flow
```
