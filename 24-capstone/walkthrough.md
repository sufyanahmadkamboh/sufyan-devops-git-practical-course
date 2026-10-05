# Capstone · reference walkthrough

> The solution of the [capstone](README.md), step by step. Try the capstone on your own first; use this when you are
> stuck or to compare. Part 1 is local; part 2 publishes to GitHub (your account) and runs the full pipeline.

## Part 1 · Repair the repository locally

### Lab setup

From the course folder: create the broken repository, and copy the grader and the workflow files next to it:

<!-- test: contains=capstone ready -->
```bash
bash 24-capstone/start-capstone.sh
cp 24-capstone/check-capstone.sh ~/git-practice/
rm -rf ~/git-practice/capstone-workflows && cp -r 21-devops-workflow/devops-project/.github/workflows ~/git-practice/capstone-workflows
cd ~/git-practice/capstone
```

### 1. Assess the damage

<!-- test: contains=MISSING; output -->
```bash
bash ../check-capstone.sh 2>&1 | grep -E "MISSING|missing"
```

```text
MISSING  clean history: no wip/asdf/fix/changes messages
MISSING  Conventional Commits on main (merges excepted)
MISSING  no .env in any commit
MISSING  no password in any commit
MISSING  .gitignore ignores .env
MISSING  chai on main, latte at the agreed 3.40
MISSING  repository checks pass on main
MISSING  CI and release workflows
MISSING  annotated tag v1.0.0 on main
MISSING  no badly named tags
10 requirement(s) missing
```

<!-- test: contains=promo-video.mp4; output -->
```bash
git log --oneline --graph --all
git log --all --format='%h %s' -- .env
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' | awk '$1 == "blob" && $2 > 1000000'
bash scripts/ci.sh | grep FAIL
```

```text
* adf80a9 (HEAD -> main) changes
| * 1850ac5 (feature/chai) chai + latte
|/  
* 5e9b2c9 (tag: release1) fix again
* ad952ec fix
* 0b1477b asdf
* ca7bff2 wip
* b42fdfa first commit
5e9b2c9 fix again
ca7bff2 wip
blob 3000000 assets/promo-video.mp4
FAIL  image tag matches VERSION (1.0.0)
```

Nothing is pushed anywhere yet: the history can be rewritten freely (lessons 31, 63, 90).

### 2. Remove the secret and the large file from every commit

The password is fake here; with a real one, **rotate it first** (lesson 89).

<!-- test: contains=0; output -->
```bash
git filter-repo --force --invert-paths --path .env --path assets/promo-video.mp4 > /dev/null 2>&1
git log --all --format=%h -- .env assets/promo-video.mp4 | wc -l
git log --oneline --graph --all
```

```text
0
* f239ec5 (HEAD -> main) changes
| * f68f2d7 (feature/chai) chai + latte
|/  
* 82c2d3d (tag: release1) fix
* 5c60dc0 wip
* b42fdfa first commit
```

The commits "asdf" and "fix again" only touched the removed files, so `filter-repo` dropped them (they became empty).

### 3. Rewrite the history into Conventional Commits

A small "editor" script maps each old message to a proper one; the `changes` commit stops for editing, because it
also broke the image tag (it must follow `VERSION`):

<!-- test: contains=reword.sh -->
```bash
cat > ../reword.sh << 'EOF'
#!/bin/sh
# reword.sh MESSAGE_FILE: replace the old subject with a Conventional Commit subject
case "$(head -n 1 "$1")" in
  "first commit") new="chore: initial cafe repository" ;;
  "wip")          new="feat(site): new home page heading" ;;
  "fix")          new="docs: add the README" ;;
  *)              exit 0 ;;
esac
printf '%s\n' "$new" > "$1"
EOF
echo "reword.sh ready"
```

<!-- test: contains=Stopped at; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i -e 's/^pick \([0-9a-f]*\) # changes$/edit \1 # changes/' -e 's/^pick/reword/'" \
  GIT_EDITOR="sh ../reword.sh" git rebase -i --root 2>&1 | grep -E "Stopped|error" || true
git status | head -3
```

```text
Rebasing (4/4)
Stopped at f239ec5...  # changes
interactive rebase in progress; onto b17589f
Last commands done (4 commands done):
   reword 82c2d3d # fix
```

At the stop: undo the image tag change, keep the latte price, and give the commit a proper message:

<!-- test: contains=Successfully rebased; output -->
```bash
git checkout HEAD~1 -- helm/cafe/values.yaml
git commit -q --amend -m "fix(menu): latte costs 3.30"
git rebase --continue 2>&1 | tail -1
git log --oneline
```

```text
Successfully rebased and updated refs/heads/main.
4ee0802 (HEAD -> main) fix(menu): latte costs 3.30
9a7dd73 docs: add the README
7440141 feat(site): new home page heading
91affa5 chore: initial cafe repository
```

### 4. Ignore what never belongs in the repository

<!-- test: contains=all checks passed; output -->
```bash
printf '.env\n*.log\n.DS_Store\nassets/*.mp4\n' > .gitignore
git add .gitignore && git commit -q -m "chore: ignore local and large files"
bash scripts/ci.sh | tail -1
```

```text
all checks passed
```

### 5. Bring the feature branch up to date and resolve its conflict

The chai branch also changed the latte price (3.50 vs 3.30 on `main`). The team agreed on 3.40:

<!-- test: contains=Successfully rebased; output -->
```bash
git switch -q feature/chai
git rebase main > /dev/null 2>&1 || true
git status --short
cat > application/menu.json << 'EOF'
{
  "items": [
    {"name": "espresso", "price": "2.50"},
    {"name": "latte", "price": "3.40"},
    {"name": "cappuccino", "price": "3.40"},
    {"name": "chai", "price": "3.10"}
  ]
}
EOF
git add application/menu.json
git -c core.editor=true rebase --continue 2>&1 | tail -1
git commit -q --amend -m "feat(menu): add chai; latte at the agreed 3.40"
git switch -q main
```

```text
UU application/menu.json
Successfully rebased and updated refs/heads/feature/chai.
```

### 6. The CI and release workflows, on their own branch

<!-- test: contains=ci.yml -->
```bash
git switch -q -c ci/workflows
mkdir -p .github && cp -r ../capstone-workflows .github/workflows
git add .github && git commit -q -m "ci: add the CI and release workflows"
ls .github/workflows
git switch -q main
git tag -d release1
```

### 7. Local result

<!-- test: contains=ok       clean history; output -->
```bash
git log --oneline --graph --all
bash ../check-capstone.sh | grep -v "^$"
```

```text
* 1b2c760 (ci/workflows) ci: add the CI and release workflows
| * ff1afd7 (feature/chai) feat(menu): add chai; latte at the agreed 3.40
|/  
* 75b72df (HEAD -> main) chore: ignore local and large files
* 4ee0802 fix(menu): latte costs 3.30
* 9a7dd73 docs: add the README
* 7440141 feat(site): new home page heading
* 91affa5 chore: initial cafe repository
== the repository
ok       clean history: no wip/asdf/fix/changes messages
ok       Conventional Commits on main (merges excepted)
ok       no .env in any commit
ok       no password in any commit
ok       no file over 1 MB in any commit
ok       .gitignore ignores .env
MISSING  chai on main, latte at the agreed 3.40
ok       repository checks pass on main
MISSING  CI and release workflows
ok       README and CONTRIBUTING
MISSING  annotated tag v1.0.0 on main
ok       no badly named tags
3 requirement(s) missing
```

Everything local is fixed except what only exists after the pull requests: chai and the workflows on `main`, and the release
tag. Part 2 does that on GitHub.

## Part 2 · Publish, protect, review, release, deploy

You need `gh` logged in (lesson 45) and Git authenticated for HTTPS (lesson 48). The repository is created as
`git-course-capstone` under your account. The outputs below are from the recorded run that built
[sufyanahmadkamboh/git-course-capstone](https://github.com/sufyanahmadkamboh/git-course-capstone) (a one-time run:
it creates the repository and protects `main`, so the test suite does not repeat it).

<!-- test-run github: gh auth setup-git -->

### 8. Create the repository and push `main`

<!-- test: skip; contains=refs/heads/main; output -->
```bash
cd ~/git-practice/capstone
gh repo create git-course-capstone --public --description "Git course capstone: a professional DevOps repository" \
  --source . --remote origin --push 2>&1 | tail -1
git push -q origin feature/chai ci/workflows 2> /dev/null
git ls-remote --heads origin
```

```text
branch 'main' set up to track 'origin/main'.
1b2c760177e51d8fca0952385b370f474524fadf	refs/heads/ci/workflows
ff1afd7f4ca31adf2b7ba561e5e72d5e55a4df6a	refs/heads/feature/chai
75b72dfd43f4f355775c87291ee2ed1941045d56	refs/heads/main
```

### 9. Protect `main`

Pull requests required (0 approvals: a solo learner cannot approve their own PRs; a team uses 1–2), the `checks` job
required and up to date, rules enforced for admins, no force pushes or deletions:

<!-- test: skip; contains=checks; output -->
```bash
me=$(gh api user --jq .login)
printf '{"required_status_checks":{"strict":true,"contexts":["checks"]},"enforce_admins":true,"required_pull_request_reviews":{"required_approving_review_count":0},"restrictions":null,"allow_force_pushes":false,"allow_deletions":false}' |
  gh api -X PUT "repos/$me/git-course-capstone/branches/main/protection" --input - \
  --jq '"required checks: \(.required_status_checks.contexts | join(", ")), force pushes: \(.allow_force_pushes.enabled)"'
```

```text
required checks: checks, force pushes: false
```

### 10. Pull request 1: the workflows

<!-- test: skip; contains=/pull/; output -->
```bash
gh pr create --base main --head ci/workflows --title "ci: add the CI and release workflows" \
  --body "Runs scripts/ci.sh, helm lint and a Docker build on every PR; tags v* build the image, push it to GHCR, create the release and deploy it to a kind cluster."
```

```text
https://github.com/sufyanahmadkamboh/git-course-capstone/pull/1
```

The checks run on the pull request; wait for them, add a review comment, merge:

<!-- test: skip; contains=pass; output -->
```bash
sleep 10
gh pr checks ci/workflows --watch > /dev/null 2>&1 || true
gh pr checks ci/workflows
gh pr review ci/workflows --comment --body "Actions are pinned by commit SHA and the release job has least-privilege permissions. Good to go."
gh pr merge ci/workflows --squash --delete-branch 2>&1 | tail -1
```

```text
checks	pass	7s	https://github.com/sufyanahmadkamboh/git-course-capstone/actions/runs/37256088398/job/111593351955	
```

In a script `gh pr review` and `gh pr merge` print nothing on success; `--delete-branch` also deletes the branch on
GitHub and locally, and updates the local `main`.

### 11. Pull request 2: the feature (update it first: `main` moved)

<!-- test: skip; contains=create mode; output -->
```bash
git fetch -q origin
git switch -q feature/chai && git rebase -q origin/main && git push -q --force-with-lease origin feature/chai 2> /dev/null
gh pr create --base main --head feature/chai --title "feat(menu): add chai" \
  --body "Adds chai (3.10). The latte price was agreed at 3.40 (conflict with main resolved)." > /dev/null
sleep 10
gh pr checks feature/chai --watch > /dev/null 2>&1 || true
gh pr review feature/chai --comment --body "Prices checked against the menu board."
gh pr merge feature/chai --squash --delete-branch 2>&1 | tail -1
```

```text
 create mode 100644 .github/workflows/release.yml
```

(The last line comes from `gh` updating your local `main` after the squash merge.)

A direct push to `main` is now impossible, even for the owner:

<!-- test: skip; contains=Protected branch update failed; output -->
```bash
git switch -q main && git pull -q
git commit -q --allow-empty -m "chore: direct push test"
git push 2>&1 | grep -E "GH006|rejected" ; git reset -q --hard origin/main
```

```text
remote: error: GH006: Protected branch update failed for refs/heads/main.        
 ! [remote rejected] main -> main (protected branch hook declined)
```

### 12. Release v1.0.0: tag → Actions → Docker → GHCR → Helm → Kubernetes

<!-- test: skip; contains=[new tag]; output -->
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0 2>&1 | tail -1
```

```text
 * [new tag]         v1.0.0 -> v1.0.0
```

The tag starts the `release` workflow: checks, image build and push to GHCR, a GitHub release with the packaged chart,
then a `deploy` job that creates a kind cluster on the runner, pulls the image from GHCR and installs the chart:

<!-- test: skip; contains=completed success; output -->
```bash
sleep 15
run=$(gh run list --workflow release --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json status,conclusion,jobs --jq '"\(.status) \(.conclusion)", (.jobs[] | "  job \(.name): \(.conclusion)")'
```

```text
completed success
  job release: success
  job deploy: success
```

<!-- test: skip; contains=cafe-1.0.0.tgz; output -->
```bash
gh release view v1.0.0 --json tagName,name,assets --jq '"\(.name) (\(.tagName))", (.assets[] | "  asset: \(.name)")'
run=$(gh run list --workflow release --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$run" --log | grep -E "Successfully|deployment.apps/cafe|chai" | sed -E 's/^[^\t]*\t[^\t]*\t[0-9TZ:.-]+ //' | head -6
```

```text
Cafe v1.0.0 (v1.0.0)
  asset: cafe-1.0.0.tgz
HEAD is now at 10a7945 feat(menu): add chai; latte at the agreed 3.40 (#2)
Successfully packaged chart and saved it to: /home/runner/work/git-course-capstone/git-course-capstone/cafe-1.0.0.tgz
HEAD is now at 10a7945 feat(menu): add chai; latte at the agreed 3.40 (#2)
deployment.apps/cafe   2/2     2            2           4s    cafe         ghcr.io/sufyanahmadkamboh/git-course-capstone:1.0.0   app.kubernetes.io/name=cafe
    {"name": "chai", "price": "3.10"}
```

### 13. Final check

<!-- test: skip; contains=capstone complete; output -->
```bash
bash ../check-capstone.sh "$(gh api user --jq .login)/git-course-capstone"
```

```text
== the repository
ok       clean history: no wip/asdf/fix/changes messages
ok       Conventional Commits on main (merges excepted)
ok       no .env in any commit
ok       no password in any commit
ok       no file over 1 MB in any commit
ok       .gitignore ignores .env
ok       chai on main, latte at the agreed 3.40
ok       repository checks pass on main
ok       CI and release workflows
ok       README and CONTRIBUTING
ok       annotated tag v1.0.0 on main
ok       no badly named tags
== GitHub (sufyanahmadkamboh/git-course-capstone)
ok       main is protected (pull requests required)
ok       force pushes to main are blocked
ok       status check required on main
ok       at least one merged pull request
ok       release v1.0.0 with the Helm chart
ok       the release workflow (build, GHCR, deploy) succeeded
ok       the latest CI run on main succeeded

capstone complete
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/capstone ~/git-practice/reword.sh ~/git-practice/check-capstone.sh ~/git-practice/capstone-workflows
```

Keep the GitHub repository as a portfolio piece, or delete it (`gh repo delete git-course-capstone`, needs the
`delete_repo` permission).
