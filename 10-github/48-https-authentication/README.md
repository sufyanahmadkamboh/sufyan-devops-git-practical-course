# Lesson 48 · HTTPS authentication

> Level 10 · Authentication · ⏱ 20 minutes

## What are we learning?

How Git proves who you are to GitHub over HTTPS: not with your account password (GitHub stopped accepting it for Git in
2021), but with a token, handed to Git by a **credential helper** so you never type it.

## Visual

```text
 git push https://github.com/YOU/repo.git
    │
    │ 401: who are you?
    ▼
 credential helper  ──►  returns username + TOKEN (stored in the OS keychain / gh's login)
    │                    Git Credential Manager (Windows, macOS, Linux), osxkeychain, gh auth git-credential
    ▼
 GitHub checks the token: valid? not expired? allowed for this repository (scopes / fine-grained permissions)?
```

| Credential | Use |
|---|---|
| Account password | the website only (with 2FA); **never** accepted by Git |
| Personal access token (fine-grained) | Git and API, limited to chosen repositories and permissions, with an expiry |
| `gh auth login` / Git Credential Manager | log in once in the browser; the token is stored and handed to Git |
| `GITHUB_TOKEN` | the automatic, short-lived token inside GitHub Actions |

## Lab setup

A fresh computer: a lab connected to your practice repository, and no credential helper configured.

<!-- test: contains=lesson-48 -->
```bash
bash scripts/new-lab.sh lesson-48 basic
cd ~/git-practice/lesson-48
```

<!-- test-run github: git config --global --unset-all credential.https://github.com.helper || true -->
<!-- test-run github: git config --global --unset-all credential.https://gist.github.com.helper || true -->

<!-- test: github; output -->
```bash
me=$(gh api user --jq .login)
git remote add origin "https://github.com/$me/git-practice-cafe.git"
git config --show-origin --get-regexp '^credential' || echo "no credential helper configured"
```

```text
no credential helper configured
```

## Demonstration

Reading a public repository needs no credentials:

<!-- test: github; contains=refs/heads/main; output -->
```bash
git ls-remote --heads origin
```

```text
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/main
```

Writing does. With no helper, Git has to ask (here prompts are disabled, so it stops; on your computer you would see
`Username for 'https://github.com':`):

<!-- test: github; fail; contains=could not read Username; output -->
```bash
git push --dry-run origin main 2>&1
```

```text
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh auth login` | log in to GitHub in the browser, store a token |
| `gh auth setup-git` | make Git use gh's token for github.com |
| `git config --global credential.helper manager` | Git Credential Manager (installed with Git for Windows) |
| `git config --show-origin --get-regexp '^credential'` | which helper is configured, and where |
| `gh auth status` | which account, which token scopes |

## Hands-on exercise

**Instructions.** After the fix below, show which credential helper Git uses for github.com and in which file it is
configured.

**Expected result.** gh's `auth git-credential` command (or `manager` if you use Git Credential Manager), in `~/.gitconfig`.

<!-- test-run github: gh auth setup-git -->

**Verification.**

<!-- test: github; contains=auth git-credential -->
```bash
git config --show-origin --get-all credential.https://github.com.helper
```

<!-- test-run github: git config --global --unset-all credential.https://github.com.helper || true -->

## Break it

Do what many people try first: answer the prompt with the **account password**. (Putting `user:password` in the URL is
the same as typing them at the prompt.)

<!-- test: github; fail; contains=Password authentication is not supported; output -->
```bash
me=$(gh api user --jq .login)
git push --dry-run "https://$me:my-account-password@github.com/$me/git-practice-cafe.git" main 2>&1
```

```text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/sufyanahmadkamboh/git-practice-cafe.git/'
```

## Troubleshoot

`Invalid username or token. Password authentication is not supported for Git operations.`: GitHub accepts only tokens
over HTTPS. Even a correct password fails. If you are asked for a "password", what Git really needs is a token, and the
comfortable way is a helper that supplies it.

## Fix

Log in once with the GitHub CLI (`gh auth login`, done in lesson 45) and connect it to Git:

<!-- test: github; contains=Everything up-to-date; output -->
```bash
gh auth setup-git
git push --dry-run origin main 2>&1
```

```text
Everything up-to-date
```

`Everything up-to-date`: Git authenticated (with gh's token), compared the branches and found nothing to push.
`--dry-run` never changes anything on GitHub.

## Real-world example

CI systems outside GitHub (Jenkins, GitLab runners, Argo CD) need a token to clone private repositories. Use a
**fine-grained** token limited to the repositories it needs, read-only if it only clones, with an expiry date, stored in
the CI's secret store, never in the repository (lesson 89). Inside GitHub Actions, use the automatic `GITHUB_TOKEN`
instead of a personal token.

## Practice challenge

Which scopes does your current `gh` token have, and which one allows pushing to repositories?

<details>
<summary>Solution</summary>

<!-- test: github; contains=repo; output -->
```bash
gh auth status --active 2>&1 | grep -i scopes
```

```text
  - Token scopes: 'gist', 'read:org', 'repo', 'user', 'workflow'
```

`repo` gives full access to your repositories (pushing included); `workflow` is additionally needed to push changes
to `.github/workflows/` files.

</details>

## Recap

- GitHub never accepts your account password for Git; HTTPS needs a token.
- A credential helper (Git Credential Manager, `gh auth setup-git`) stores and supplies it.
- Prefer fine-grained, expiring, least-privilege tokens; in Actions use `GITHUB_TOKEN`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-48
```

Next: [Lesson 49 · SSH authentication](../49-ssh-authentication/README.md).
