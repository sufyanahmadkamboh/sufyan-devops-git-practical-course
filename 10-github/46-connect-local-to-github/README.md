# Lesson 46 · Connecting local Git to GitHub

> Level 9 · GitHub fundamentals · ⏱ 15 minutes

## What are we learning?

How to push an existing local repository into the empty GitHub repository from lesson 45: add the remote, push with
upstream. Exactly what GitHub's "…or push an existing repository from the command line" box tells you.

## Visual

```text
 local repository (3 commits)          github.com/YOU/git-practice-cafe (empty)
 main ──────────────────────────────►  main
        git remote add origin URL
        git push -u origin main
```

## Lab setup

<!-- test: contains=lesson-46 -->
```bash
bash scripts/new-lab.sh lesson-46 basic
cd ~/git-practice/lesson-46
git log --oneline
```

<!-- test-run github: gh auth setup-git -->

Your account name, used in the URLs below:

<!-- test: github; output -->
```bash
me=$(gh api user --jq .login)
echo "$me"
```

```text
sufyanahmadkamboh
```

## Demonstration

<!-- test: github; contains=git-practice-cafe.git; output -->
```bash
me=$(gh api user --jq .login)
git remote add origin "https://github.com/$me/git-practice-cafe.git"
git remote -v
```

```text
origin	https://github.com/sufyanahmadkamboh/git-practice-cafe.git (fetch)
origin	https://github.com/sufyanahmadkamboh/git-practice-cafe.git (push)
```

The first push creates `main` on GitHub and connects your local `main` to it:

<!-- test: skip; contains=[new branch]; output -->
```bash
git push -u origin main
```

```text
To https://github.com/sufyanahmadkamboh/git-practice-cafe.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

(If Git asks for a username and password here, read lesson 48 first: GitHub does not accept your account password.)

<!-- test: github; contains=4267004; output -->
```bash
git fetch -q
git branch -vv
git ls-remote --heads origin
```

```text
* main 4267004 [origin/main] Add prices
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/main
```

The commit IDs on GitHub are the same as on your computer: it is the same history.

## Command breakdown

| Command | What it does |
|---|---|
| `git remote add origin URL` | connect the local repository to GitHub |
| `git push -u origin main` | upload `main`, set its upstream |
| `git branch -M main` | rename the current branch to `main` (GitHub's snippet includes it for old `master` setups) |
| `gh repo create NAME --source . --push` | create the GitHub repository and push in one step |

## Hands-on exercise

**Instructions.** Open the repository page and confirm the three files are there, using the CLI.

**Expected result.** `README.md`, `menu.txt`, `prices.txt`.

**Verification.**

<!-- test: github; contains=prices.txt -->
```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/contents" --jq '.[].name'
```

## Break it

A typo in the repository name when adding the remote:

<!-- test: github; fail; contains=not found; output -->
```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practise-cafe.git"
git push 2>&1
```

```text
remote: Repository not found.
fatal: repository 'https://github.com/sufyanahmadkamboh/git-practise-cafe.git/' not found
```

## Troubleshoot

`remote: Repository not found.` Now that Git is authenticated (unlike lesson 44), GitHub says it clearly: under this
owner there is no repository with that name, or you have no access to it. Compare the remote URL with the page URL:

<!-- test: github; contains=git-practise-cafe -->
```bash
git remote get-url origin
```

## Fix

<!-- test: github; contains=Everything up-to-date; output -->
```bash
me=$(gh api user --jq .login)
git remote set-url origin "https://github.com/$me/git-practice-cafe.git"
git push 2>&1
```

```text
Everything up-to-date
```

## Real-world example

Migrating a project from another server (an old GitLab, a bare repository on a VM) to GitHub: clone it with
`git clone --mirror`, create the empty GitHub repository, `git push --mirror` to it. All branches and tags arrive with
their history and the same commit IDs.

## Practice challenge

Create a branch `docs`, push it with upstream, and list the branches that exist on GitHub.

<details>
<summary>Solution</summary>

<!-- test: github; contains=refs/heads/docs; output -->
```bash
cd ~/git-practice/lesson-46
git switch -q -c docs
git push -q -u origin docs 2>&1
git ls-remote --heads origin
git push -q origin --delete docs 2>&1
```

```text
remote: 
remote: Create a pull request for 'docs' on GitHub by visiting:        
remote:      https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/new/docs        
remote: 
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/docs
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/main
```

The last line deletes the branch on GitHub again, to keep the practice repository tidy.

</details>

## Recap

- `git remote add origin URL` + `git push -u origin main` publishes a local repository.
- An authenticated `Repository not found` means a wrong owner/name or no access.
- The commit IDs are identical locally and on GitHub.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-46
```

Next: [Lesson 47 · GitHub repository structure](../47-github-repository-structure/README.md).
