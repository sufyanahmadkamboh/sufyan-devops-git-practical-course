# Module 24 · Final capstone

> Level 25 · ⏱ 4–6 hours · everything in the course · needs a GitHub account

## The challenge

A team left you its repository in a bad state: meaningless commit messages, a password in the history, a large video
in the history, no `.gitignore`, a version mismatch that fails CI, a feature branch that conflicts with `main`, a
badly named tag, and no CI at all. Turn it into a **professional GitHub repository** with a complete delivery
pipeline:

```text
 Developer → Git → GitHub → feature branch → Pull Request → review → checks → merge → tag
     → release → GitHub Actions → Docker image → GHCR → Helm → Kubernetes
```

## Start

<!-- test: contains=capstone ready -->
```bash
bash 24-capstone/start-capstone.sh
cp 24-capstone/check-capstone.sh ~/git-practice/
```

The repository is in `~/git-practice/capstone`. It is the cafe DevOps repository from
[module 21](../21-devops-workflow/README.md): website, Dockerfile, Helm chart, scripts. Its CI and release workflows are
in [21-devops-workflow/devops-project/.github/workflows](../21-devops-workflow/devops-project/.github/workflows/).

## Requirements

**Clean, safe history** (nothing is pushed yet, so you may rewrite everything)

1. Conventional Commit messages throughout; no `wip`, `asdf`, `fix`, `changes`.
2. No `.env`, no password, no file over 1 MB in **any** commit; `.gitignore` keeps them out from now on.
3. The image tag in `helm/cafe/values.yaml` follows `VERSION`; `scripts/ci.sh` passes on `main`.
4. No badly named tags; releases use annotated semantic version tags.

**Professional GitHub repository**

5. A public repository on your account; `main` protected: pull requests required, the CI check required and up to
   date, enforced for admins, no force pushes or deletions.
6. The workflows arrive through a pull request, with green checks and a review comment.
7. `feature/chai` arrives through a pull request: updated with `main`, its conflict resolved (latte at the agreed
   **3.40**), green checks, merged.
8. Documentation: README and `docs/CONTRIBUTING.md`.

**Release and deployment**

9. An annotated tag `v1.0.0` on `main` triggers the release workflow, which must succeed: the image built and pushed
   to GHCR, a GitHub release with the packaged Helm chart, and a deployment of that image with Helm to a Kubernetes
   (kind) cluster, verified by a smoke test.

## Grade yourself

Inside your capstone repository, the local part:

<!-- test: skip -->
```bash
bash ../check-capstone.sh
```

and, after publishing, the GitHub part too:

<!-- test: skip -->
```bash
bash ../check-capstone.sh YOUR-ACCOUNT/git-course-capstone
```

`capstone complete` = done.

## Hints

| Requirement | Lessons |
|---|---|
| history rewriting | 63 (interactive rebase), 66 (edit stops), 90 (`git filter-repo`) |
| secrets, large files | 89, 90, 88, 73 |
| conflicts | 26, 27, 64 |
| GitHub, protection, PRs | 45–47, 52–54, 59 |
| tags, releases, Actions | 68, 69, 97, 98, module 21 |
| Docker, Helm, Kubernetes | project 6 |

## Reference

A complete, recorded run of the capstone (on the repository
[git-course-capstone](https://github.com/sufyanahmadkamboh/git-course-capstone)) is in [walkthrough.md](walkthrough.md).
Then take the [final exam](final-exam/README.md).

<!-- test -->
```bash
rm -rf ~/git-practice/capstone ~/git-practice/check-capstone.sh
```
