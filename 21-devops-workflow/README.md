# Module 21 · Professional DevOps Git workflow

> Level 21 · DevOps workflow · ⏱ 60 minutes · run every command from the course folder (`git-practical-course/`)

## What are we learning?

Everything from the previous modules, in the order a DevOps team uses it every day, on a realistic repository:
an application, a Dockerfile, a Helm chart, Kubernetes manifests, scripts, documentation and CI workflows. One change
goes from a developer's branch all the way to production.

## Visual

```text
 Developer ─► Feature branch ─► Commit ─► Push ─► Pull Request ─► Review ─► CI ─► Merge ─► Release ─► Deployment
   Ada        feat/add-chai     feat(…)   origin   branch vs main   Grace    ci.sh  --no-ff   v1.1.0     production/
                                                                                              (tag)      (deploy.sh)
```

The repository ([devops-project/](devops-project/)):

```text
devops-project/
├── application/          index.html, menu.json            the website
├── Dockerfile            nginx (non-root) serving application/
├── VERSION               1.0.0: the single source of truth for the version
├── helm/cafe/            Chart.yaml (appVersion), values.yaml (image tag), templates/
├── kubernetes/           namespace.yaml
├── scripts/              ci.sh · release.sh · deploy.sh
├── docs/                 CONTRIBUTING.md (the team's workflow)
└── .github/workflows/    ci.yml (PRs, main) · release.yml (tags v*: image → GHCR, GitHub release)
```

On GitHub the pull request, review and CI happen on github.com (modules 10–12, 20); here the "server" is a local
bare repository and the CI is `scripts/ci.sh`, the same script the GitHub workflow runs. The capstone (module 24) does
the whole flow on GitHub.

## Lab setup

Create the team's repository from the template, publish it on the "server", and give Grace (the reviewer) a clone:

<!-- test: contains=devops-server.git -->
```bash
bash scripts/new-lab.sh devops empty
cp -r 21-devops-workflow/devops-project/. ~/git-practice/devops/
cd ~/git-practice/devops
git add . && git commit -q -m "chore: initial cafe DevOps repository"
git tag -a v1.0.0 -m "Release 1.0.0"
git init -q --bare ../devops-server.git && git remote add origin ../devops-server.git
git push -q -u origin main --follow-tags
git clone -q ../devops-server.git ../devops-grace
git -C ../devops-grace config user.name "Grace Hopper" && git -C ../devops-grace config user.email "grace@example.com"
git ls-remote --heads --tags ../devops-server.git | sed 's|.*\trefs/|refs/|' && echo "../devops-server.git ready"
```

The current release is live:

<!-- test: contains=deployed cafe 1.0.0; output -->
```bash
bash scripts/deploy.sh ../devops-server.git v1.0.0 ../production
```

```text
deployed cafe 1.0.0 (v1.0.0) to production
```

## Demonstration

### 1. Developer → feature branch → commit

Ada adds chai to the menu, on a branch named by convention, with a Conventional Commit message:

<!-- test: contains=feat(menu): add chai -->
```bash
git switch -q main && git pull -q
git switch -c feat/add-chai
sed -i 's/{"name": "cappuccino", "price": "3.40"}/{"name": "cappuccino", "price": "3.40"},\n    {"name": "chai", "price": "3.10"}/' application/menu.json
git diff --stat
git commit -q -am "feat(menu): add chai"
git log --oneline -1
```

### 2. CI locally, then push

<!-- test: contains=all checks passed; output -->
```bash
bash scripts/ci.sh
git push -q -u origin feat/add-chai
```

```text
ok    menu.json is valid JSON
ok    every menu item has a price with two decimals
ok    VERSION is semantic (MAJOR.MINOR.PATCH)
ok    Chart appVersion matches VERSION (1.0.0)
ok    image tag matches VERSION (1.0.0)
ok    no secrets in tracked files
all checks passed
```

### 3. Pull request → review → CI

The PR is "merge `feat/add-chai` into `main`". Grace reviews exactly what GitHub would show (lesson 51) and runs the
checks on the branch (what `ci.yml` does on every PR):

<!-- test: contains=+    {"name": "chai", "price": "3.10"}; contains=all checks passed; output -->
```bash
cd ../devops-grace && git fetch -q
git log --oneline main..origin/feat/add-chai
git diff main...origin/feat/add-chai
git switch -q --detach origin/feat/add-chai && bash scripts/ci.sh | tail -1 && git switch -q main
```

```text
45125aa (origin/feat/add-chai) feat(menu): add chai
diff --git a/application/menu.json b/application/menu.json
index 6ed58dd..e10981d 100644
--- a/application/menu.json
+++ b/application/menu.json
@@ -2,6 +2,7 @@
   "items": [
     {"name": "espresso", "price": "2.50"},
     {"name": "latte", "price": "3.20"},
-    {"name": "cappuccino", "price": "3.40"}
+    {"name": "cappuccino", "price": "3.40"},
+    {"name": "chai", "price": "3.10"}
   ]
 }
all checks passed
```

### 4. Merge

Approved and green: merged with a merge commit (the PR button), and the branch is deleted:

<!-- test: contains=Merge pull request; output -->
```bash
git merge -q --no-ff -m "Merge pull request #1 from feat/add-chai" origin/feat/add-chai
git push -q && git push -q origin --delete feat/add-chai
git log --oneline --graph -4
```

```text
*   5755737 (HEAD -> main, origin/main, origin/HEAD) Merge pull request #1 from feat/add-chai
|\  
| * 45125aa feat(menu): add chai
|/  
* 73ad8bc (tag: v1.0.0) chore: initial cafe DevOps repository
```

### 5. Release

Ada updates `main` and releases 1.1.0 (a new feature: minor version). The script sets the version in `VERSION`, the
chart and the image tag, re-runs the checks, commits and tags:

<!-- test: contains=released v1.1.0; output -->
```bash
cd ../devops && git switch -q main && git pull -q && git branch -d feat/add-chai
bash scripts/release.sh 1.1.0
git push -q --follow-tags
git log --oneline --decorate -2
```

```text
Deleted branch feat/add-chai (was 45125aa).
released v1.1.0: push with  git push --follow-tags
4e4ff72 (HEAD -> main, tag: v1.1.0, origin/main, origin/HEAD) chore(release): 1.1.0
5755737 Merge pull request #1 from feat/add-chai
```

On GitHub, pushing the tag `v1.1.0` starts `release.yml`: image `ghcr.io/…/cafe:1.1.0` and a GitHub release with
the packaged chart.

### 6. Deployment

<!-- test: contains=deployed cafe 1.1.0; output -->
```bash
bash scripts/deploy.sh ../devops-server.git v1.1.0 ../production
grep -c '"name"' ../production/application/menu.json
```

```text
deployed cafe 1.1.0 (v1.1.0) to production
4
```

Production serves four items; the deployed version is exactly the tagged commit.

## Command breakdown

| Step | Commands | Lesson |
|---|---|---|
| start | `git switch main && git pull && git switch -c feat/…` | 20, 41, 56 |
| commit | `git add`, `git commit -m "feat(scope): …"` | 09–11, 84 |
| check + push | `bash scripts/ci.sh`, `git push -u origin feat/…` | 42–43 |
| review | `git log main..BRANCH`, `git diff main...BRANCH`, `gh pr review` | 51–53 |
| merge | PR merge button / `git merge --no-ff` | 23–25, 54 |
| release | `scripts/release.sh X.Y.Z` → annotated tag, `git push --follow-tags` | 68–69, 97 |
| deploy | `deploy.sh` (real life: `docker build/push`, `helm upgrade --install --set image.tag=X.Y.Z`) | 98 |

## Hands-on exercise

**Instructions.** Show which commits went into release 1.1.0 since 1.0.0, without merges: the material for its
release notes.

**Expected result.** "feat(menu): add chai" and "chore(release): 1.1.0".

**Verification.**

<!-- test: contains=feat(menu): add chai; contains=chore(release): 1.1.0 -->
```bash
cd ~/git-practice/devops
git log --oneline --no-merges v1.0.0..v1.1.0
```

## Break it

The next change: Ada raises the latte price and, "while she is at it", bumps the image tag by hand. She skips the
local checks and pushes the branch:

<!-- test: fail; contains=FAIL  image tag matches VERSION; output -->
```bash
git switch -q -c fix/latte-price
sed -i 's/"latte", "price": "3.20"/"latte", "price": "3.30"/' application/menu.json
sed -i 's/tag: "1.1.0"/tag: "1.1.1"/' helm/cafe/values.yaml
git commit -q -am "fix(menu): latte costs 3.30" && git push -q -u origin fix/latte-price
cd ../devops-grace && git fetch -q && git switch -q --detach origin/fix/latte-price
bash scripts/ci.sh
```

```text
ok    menu.json is valid JSON
ok    every menu item has a price with two decimals
ok    VERSION is semantic (MAJOR.MINOR.PATCH)
ok    Chart appVersion matches VERSION (1.1.0)
FAIL  image tag matches VERSION (1.1.0)
ok    no secrets in tracked files
checks failed
```

## Troubleshoot

The PR's CI is red: `image tag matches VERSION` failed. `values.yaml` now says `1.1.1` while `VERSION` and the chart
say `1.1.0`: the deployment would run an image that was never built. In review, Grace points at the line:

<!-- test: contains=tag: "1.1.1"; output -->
```bash
git diff origin/main...origin/fix/latte-price -- helm/
git switch -q main
```

```text
diff --git a/helm/cafe/values.yaml b/helm/cafe/values.yaml
index 7fd6967..8803cc1 100644
--- a/helm/cafe/values.yaml
+++ b/helm/cafe/values.yaml
@@ -2,7 +2,7 @@ replicaCount: 2
 
 image:
   repository: ghcr.io/your-account/cafe
-  tag: "1.1.0"
+  tag: "1.1.1"
 
 service:
   port: 80
```

Versions are changed **only** by the release script, at release time; a PR changes the application.

## Fix

Ada removes the version change from her commit (her own branch: amend and force-push with lease, lesson 42), CI goes
green, and the PR can be merged and released as 1.1.1:

<!-- test: contains=deployed cafe 1.1.1; output -->
```bash
cd ../devops
git checkout main -- helm/cafe/values.yaml
git commit -q --amend --no-edit && bash scripts/ci.sh | tail -1
git push -q --force-with-lease
cd ../devops-grace && git fetch -q && git merge -q --no-ff -m "Merge pull request #2 from fix/latte-price" origin/fix/latte-price && git push -q && git push -q origin --delete fix/latte-price
cd ../devops && git switch -q main && git pull -q && git branch -D fix/latte-price > /dev/null
bash scripts/release.sh 1.1.1 > /dev/null && git push -q --follow-tags
bash scripts/deploy.sh ../devops-server.git v1.1.1 ../production
```

```text
all checks passed
deployed cafe 1.1.1 (v1.1.1) to production
```

## Real-world example

This is the shape of most production repositories: protected `main` (lesson 59) requiring the `ci` check and one
review; Conventional Commits (lesson 84) so release notes write themselves; tags trigger the release pipeline (image to
a registry, chart to a repository); a deployment tool (Helm in CI, or Argo CD/Flux watching the Git repository:
GitOps) makes the cluster follow what Git says. Rollback = deploy the previous tag.

## Practice challenge

Production has a problem with 1.1.1. Roll back to 1.1.0 using only the release tags.

<details>
<summary>Solution</summary>

<!-- test: contains=deployed cafe 1.1.0; output -->
```bash
cd ~/git-practice/devops
git tag -l "v*"
bash scripts/deploy.sh ../devops-server.git v1.1.0 ../production
grep latte ../production/application/menu.json
```

```text
v1.0.0
v1.1.0
v1.1.1
deployed cafe 1.1.0 (v1.1.0) to production
    {"name": "latte", "price": "3.20"},
```

Because every release is an immutable tag, rollback is a redeploy of an earlier tag; the fix then goes forward as
1.1.2.

</details>

## Recap

- The DevOps flow: branch → commit → push → PR → review → CI → merge → release (tag) → deploy.
- CI scripts in the repository run the same locally and in GitHub Actions.
- Versions change only at release; releases are tags; deployment and rollback use tags.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/devops ~/git-practice/devops-server.git ~/git-practice/devops-grace ~/git-practice/production
```

Next: [Module 22 · Real-world troubleshooting](../22-troubleshooting/README.md).
