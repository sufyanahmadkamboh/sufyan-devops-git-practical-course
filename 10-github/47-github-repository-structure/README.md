# Lesson 47 · GitHub repository structure

> Level 9 · GitHub fundamentals · ⏱ 15 minutes

## What are we learning?

What each tab of a GitHub repository page is for, which of them are plain Git (Code, Branches, Tags) and which are
GitHub features stored outside Git (Issues, Pull requests, Actions, Releases, Settings). For each tab we use the
command-line equivalent.

## Visual

```text
 github.com/YOU/git-practice-cafe
 ┌───────┬────────┬───────────────┬─────────┬──────────┬──────────┐
 │ Code  │ Issues │ Pull requests │ Actions │ Projects │ Settings │
 └───────┴────────┴───────────────┴─────────┴──────────┴──────────┘
  Code: files of the default branch, README, branch selector, "N branches", "N tags", Releases (right side)

 stored IN Git (cloned with the repository)        stored by GitHub (NOT in a clone)
   files, commits, branches, tags                    issues, PRs + reviews, Actions runs,
                                                     releases' notes and assets, settings
```

## Lab setup

<!-- test: contains=lesson-47 -->
```bash
bash scripts/new-lab.sh lesson-47 empty
cd ~/git-practice/lesson-47
```

<!-- test: github; contains=Cloning -->
```bash
me=$(gh api user --jq .login)
gh repo clone "$me/git-practice-cafe" 2>&1
cd git-practice-cafe
```

## Demonstration

**Code**, **Branches**, **Tags**: Git data, available offline after cloning:

<!-- test: github; contains=README.md; output -->
```bash
ls
git branch -r
git tag
```

```text
README.md
menu.txt
prices.txt
  origin/HEAD -> origin/main
  origin/main
```

**Issues**, **Pull requests**, **Actions**, **Releases**: GitHub data, read through the API. `gh` finds the repository
from the `origin` remote:

<!-- test: github; output -->
```bash
echo "issues:   $(gh issue list --state all --json number --jq length)"
echo "PRs:      $(gh pr list --state all --json number --jq length)"
echo "runs:     $(gh run list --json databaseId --jq length)"
echo "releases: $(gh release list --json tagName --jq length)"
```

```text
issues:   0
PRs:      0
runs:     0
releases: 0
```

**Settings**: repository options, branch protection, collaborators, secrets. Some are visible through the API:

<!-- test: github; contains=default_branch; output -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe" --jq '{default_branch, visibility, has_issues, allow_squash_merge, delete_branch_on_merge}'
```

```text
{"allow_squash_merge":true,"default_branch":"main","delete_branch_on_merge":false,"has_issues":true,"visibility":"public"}
```

## Command breakdown

| Tab | Web | CLI |
|---|---|---|
| Code | file browser, README | `git clone`, `gh repo view` |
| Branches / Tags | `/branches`, `/tags` | `git ls-remote`, `git branch -r`, `git tag` |
| Issues | `/issues` | `gh issue list / create / view` (lesson 93) |
| Pull requests | `/pulls` | `gh pr list / create / review / merge` (lesson 52) |
| Actions | `/actions` | `gh run list / view / watch` (lesson 98) |
| Releases | `/releases` | `gh release list / create` (lesson 97) |
| Settings | `/settings` | `gh repo edit`, `gh api repos/OWNER/REPO` |

## Hands-on exercise

**Instructions.** Print the URL of every tab of your practice repository.

**Expected result.** Seven URLs ending in `/issues`, `/pulls`, `/actions`, ...

**Verification.**

<!-- test: github; contains=/pulls -->
```bash
url=$(gh repo view --json url --jq .url)
for tab in "" /issues /pulls /actions /releases /branches /tags; do echo "$url$tab"; done
```

## Break it

Use `gh` outside a repository folder:

<!-- test: github; fail; contains=no git remotes found; output -->
```bash
cd ~/git-practice/lesson-47
gh issue list 2>&1
```

```text
no git remotes found
```

## Troubleshoot

`no git remotes found`: `gh` picks the repository from the current folder's Git remotes. The lab folder is a Git
repository, but without a GitHub remote, so `gh` cannot know which repository you mean. (Outside any repository the
message is `not a git repository`.)

## Fix

Name it explicitly with `-R OWNER/REPO`, or `cd` into the clone:

<!-- test: github; contains=OK -->
```bash
me=$(gh api user --jq .login)
gh issue list -R "$me/git-practice-cafe" > /dev/null && echo OK
```

## Real-world example

When you clone a repository to investigate a production issue, you get the code and its history, but not the
discussion: why a change was made usually lives in the pull request and the linked issue. `gh pr list --search SHA
--state merged` finds the PR that introduced a commit, and its review conversation.

## Practice challenge

Show the repository's README as GitHub renders it in the terminal.

<details>
<summary>Solution</summary>

<!-- test: github; contains=Cafe; output -->
```bash
cd ~/git-practice/lesson-47/git-practice-cafe
gh repo view | head -8
```

```text
name:	sufyanahmadkamboh/git-practice-cafe
description:	Practice repository for the Git Practical Course
--
# Cafe

The menu and prices of a small cafe.
```

</details>

## Recap

- Code, branches and tags are Git; issues, PRs, Actions, releases and settings are GitHub.
- A clone contains only the Git part.
- `gh` is the command-line window to the GitHub part (`-R OWNER/REPO` outside a clone).

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-47
```

Next: [Lesson 48 · HTTPS authentication](../48-https-authentication/README.md).
