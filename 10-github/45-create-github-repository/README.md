# Lesson 45 · Creating a GitHub repository

> Level 9 · GitHub fundamentals · ⏱ 15 minutes

## What are we learning?

How to create a repository on GitHub, in the web interface and with the GitHub CLI, and which options matter when you
are going to push an existing project into it.

This lesson and the following GitHub lessons need a free GitHub account. The practice repository is called
`git-practice-cafe`; you can delete it at the end of the course.

## Visual

```text
 github.com  →  "+" (top right)  →  New repository
   Owner / Repository name      your-account / git-practice-cafe
   Description                  Practice repository for the Git course
   Public | Private
   Initialize with: README / .gitignore / license
        └── leave all EMPTY when you will push an existing local repository
            (otherwise GitHub creates a first commit, and your push meets "unrelated histories", lesson 25)
   [Create repository]  →  a page with the URL and "…or push an existing repository from the command line"
```

## Lab setup

The GitHub CLI must be logged in (`gh auth login`, follow the prompts; lesson 48 explains what it configures):

<!-- test: github; output -->
```bash
gh auth status --active 2>&1 | grep -E "Logged in|scopes"
```

```text
  ✓ Logged in to github.com account sufyanahmadkamboh (keyring)
  - Token scopes: 'gist', 'read:org', 'repo', 'user', 'workflow'
```

## Demonstration

**In the browser**: follow the visual above, with no README, no .gitignore, no license.

**With the CLI**, the same in one command:

<!-- test: skip; contains=git-practice-cafe; output -->
```bash
gh repo create git-practice-cafe --public --description "Practice repository for the Git Practical Course"
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe
```

(In a terminal, gh also prints `✓ Created repository YOU/git-practice-cafe on github.com`; the URL is the part
scripts use.) The repository exists, empty:

<!-- test: github; contains=git-practice-cafe; output -->
```bash
gh repo view git-practice-cafe --json name,visibility,url --jq '"\(.name) \(.visibility) \(.url)"'
```

```text
git-practice-cafe PUBLIC https://github.com/sufyanahmadkamboh/git-practice-cafe
```

## Command breakdown

| Command / option | Meaning |
|---|---|
| `gh repo create NAME --public` / `--private` | create under your account |
| `gh repo create ORG/NAME` | create in an organisation |
| `--add-readme`, `--gitignore Go`, `--license mit` | initialise with files (a first commit) |
| `--source . --push` | create from the current local repository and push it |
| `gh repo view NAME` | show it; `--web` opens the browser |
| `gh repo delete NAME` | delete (needs the `delete_repo` permission) |

## Hands-on exercise

**Instructions.** Show the repository's default branch name and whether it is empty.

**Expected result.** `isEmpty` is `true` until you push (lesson 46).

**Verification.**

<!-- test: github; contains=isEmpty -->
```bash
gh repo view git-practice-cafe --json isEmpty,defaultBranchRef
```

## Break it

Create it a second time:

<!-- test: github; fail; contains=Name already exists on this account; output -->
```bash
gh repo create git-practice-cafe --public 2>&1
```

```text
GraphQL: Name already exists on this account (createRepository)
```

## Troubleshoot

`Name already exists on this account`: repository names are unique per owner. Either the repository is already there
(use it: `gh repo view git-practice-cafe`) or pick another name. Also check the **owner**: in an organisation, the same
name can exist under your personal account and under the organisation.

## Fix

Nothing to recreate: list your repositories and use the existing one.

<!-- test: github; contains=git-practice-cafe -->
```bash
gh repo list --limit 100 --json name --jq '.[].name' | grep -x git-practice-cafe
```

## Real-world example

In companies, repositories are usually created in the organisation (`gh repo create my-org/payments-api --private`),
often from a **template repository** that already contains the standard CI workflow, `CODEOWNERS`, `.gitignore` and
Helm chart skeleton: `gh repo create my-org/new-service --template my-org/service-template --private`.

## Practice challenge

Add topics to the repository from the command line (`gh repo edit`), then show them.

<details>
<summary>Solution</summary>

<!-- test: github; contains=git; output -->
```bash
me=$(gh api user --jq .login)
gh repo edit "$me/git-practice-cafe" --add-topic git --add-topic practice > /dev/null
gh repo view git-practice-cafe --json repositoryTopics --jq '[.repositoryTopics[].name] | join(", ")'
```

```text
git, practice
```

</details>

## Recap

- Create empty repositories when you will push an existing project.
- `gh repo create` does the same as the web form; names are unique per owner.
- Organisations and templates are the usual way in teams.

## Cleanup

Keep the repository: the next lessons use it.

Next: [Lesson 46 · Connecting local Git to GitHub](../46-connect-local-to-github/README.md).
