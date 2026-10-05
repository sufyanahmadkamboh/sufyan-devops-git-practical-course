# Problem 10 · Authentication failure

> Troubleshooting lab · run every command from the course folder · related lessons: [48](../10-github/48-https-authentication/README.md), [49](../10-github/49-ssh-authentication/README.md), [50](../10-github/50-ssh-vs-https/README.md)

## Problem

A freshly set-up laptop: `git push` to GitHub fails, over SSH and over HTTPS.

<!-- test: contains=lesson-t10 -->
```bash
bash scripts/new-lab.sh lesson-t10 basic
cd ~/git-practice/lesson-t10
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keyscan -t ed25519 github.com 2> /dev/null >> ~/.ssh/known_hosts
git remote add origin git@github.com:octocat/Hello-World.git
```

## Symptoms

<!-- test: fail; contains=Permission denied (publickey); output -->
```bash
git ls-remote origin 2>&1
```

```text
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

## Investigation

Is it the network, the host key, or the key? Ask SSH directly, with details:

<!-- test: contains=Permission denied (publickey); output -->
```bash
ssh -T git@github.com 2>&1 | tail -1
ssh -vT git@github.com 2>&1 | grep -E "Connecting to|Authenticated|Server accepts|Offering public key|No more authentication|identity file" | sed "s|$HOME|~|" | head -6
```

```text
git@github.com: Permission denied (publickey).
debug1: Connecting to github.com [140.82.121.3] port 22.
debug1: identity file ~/.ssh/id_rsa type -1
debug1: identity file ~/.ssh/id_ecdsa type -1
debug1: identity file ~/.ssh/id_ecdsa_sk type -1
debug1: identity file ~/.ssh/id_ed25519 type -1
debug1: identity file ~/.ssh/id_ed25519_sk type -1
```

For HTTPS, check what Git would send:

<!-- test: output -->
```bash
git config --show-origin --get-regexp '^credential' || echo "no credential helper configured"
```

```text
no credential helper configured
```

## Commands

| Command | Shows |
|---|---|
| `git remote -v` | SSH (`git@github.com:`) or HTTPS (`https://`) |
| `ssh -T git@github.com` | which account GitHub sees for your key ("Hi NAME!") |
| `ssh -vT git@github.com` | which keys are offered and what the server answers |
| `gh auth status` | the account and token scopes used for HTTPS (with gh as helper) |
| `git config --get-regexp ^credential` | which credential helper is configured |

## Understand the output

The connection reached GitHub (`Connecting to github.com`, host key accepted), but no offered key was accepted:
either no key exists (`identity file … not found` / no "Offering public key" line) or the key is not registered on any
GitHub account. Over HTTPS, no credential helper means Git would ask for a username and password, and GitHub rejects
account passwords for Git (lesson 48).

## Root cause

Credentials were never set up on this machine: no SSH key registered with GitHub, no token for HTTPS.

## Fix

Either protocol works; pick one.

**SSH**: create a key and register its public part on GitHub (Settings → SSH and GPG keys, or `gh ssh-key add`):

<!-- test: contains=ssh-ed25519 -->
```bash
[ -f ~/.ssh/id_ed25519 ] || ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

**HTTPS**: log in with the GitHub CLI and let it act as Git's credential helper (`gh auth login`, then):

<!-- test: github; contains=refs/heads; output -->
```bash
gh auth setup-git
git remote set-url origin https://github.com/octocat/Hello-World.git
git ls-remote --heads origin | head -2
```

```text
```

## Verification

After registering the key, `ssh -T git@github.com` answers `Hi YOUR-ACCOUNT! You've successfully authenticated…`; with
HTTPS, `git push --dry-run` succeeds without a prompt (lesson 48).

## Prevention

- One documented setup per laptop: `gh auth login` (HTTPS) or an SSH key with a passphrase, added to the agent.
- In CI, never personal credentials: `GITHUB_TOKEN`, deploy keys or short-lived app tokens.
- `Permission denied (publickey)` = authentication; `Connection timed out` = network (lesson 50).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t10
```

Next: [Problem 11 · Wrong upstream branch](problem-11-wrong-upstream.md)
