<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 48 · HTTPS authentication · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Do what many people try first: answer the prompt with the **account password**. (Putting `user:password` in the URL is
the same as typing them at the prompt.)

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

```bash
gh auth setup-git
git push --dry-run origin main:refs/heads/lesson-48-check 2>&1
```

```text
To https://github.com/sufyanahmadkamboh/git-practice-cafe.git
 * [new branch]      main -> lesson-48-check
```

Git authenticated (with gh's token) and would create the branch `lesson-48-check`; `--dry-run` stops there and never
changes anything on GitHub.
