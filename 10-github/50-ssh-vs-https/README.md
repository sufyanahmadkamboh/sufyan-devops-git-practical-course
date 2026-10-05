# Lesson 50 · SSH vs HTTPS

> Level 10 · Authentication · ⏱ 15 minutes

## What are we learning?

Both protocols reach the same repository. We compare them in practice, switch a clone from one to the other, and fix
the most common network problem: port 22 blocked by a firewall.

## Visual

```text
                         HTTPS                                  SSH
 URL                     https://github.com/YOU/repo.git        git@github.com:YOU/repo.git
 port                    443 (open almost everywhere)           22 (sometimes blocked) · or 443 via ssh.github.com
 credential              token via a credential helper          key pair (+ passphrase, ssh-agent)
 set up once             gh auth login / Git Credential Manager ssh-keygen + add the public key
 expires                 tokens: yes (by design)                keys: no (unless you rotate them)
 scope                   token permissions (fine-grained)       full access of the account (or one repo: deploy key)
 also used for           the GitHub API (gh, curl)              commit signing (lesson 91)
```

Neither is "more secure" by itself: a fine-grained expiring token and a passphrase-protected key are both good choices.
Pick one per computer and be consistent.

## Lab setup

<!-- test: contains=lesson-50 -->
```bash
bash scripts/new-lab.sh lesson-50 basic
cd ~/git-practice/lesson-50
git remote add origin https://github.com/octocat/Hello-World.git
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

## Demonstration

Switch the remote to SSH: only the URL changes; branches, history and upstreams stay.

<!-- test: contains=git@github.com:octocat/Hello-World.git; output -->
```bash
git remote set-url origin git@github.com:octocat/Hello-World.git
git remote -v
```

```text
origin	git@github.com:octocat/Hello-World.git (fetch)
origin	git@github.com:octocat/Hello-World.git (push)
```

Or let Git rewrite every GitHub HTTPS URL to SSH automatically, for all repositories:

<!-- test: contains=git@github.com:octocat; output -->
```bash
git remote set-url origin https://github.com/octocat/Hello-World.git
git config --global url."git@github.com:".insteadOf "https://github.com/"
git remote -v
git config --global --unset url."git@github.com:".insteadOf
```

```text
origin	git@github.com:octocat/Hello-World.git (fetch)
origin	git@github.com:octocat/Hello-World.git (push)
```

`git remote -v` already shows the rewritten URL; the config file still says HTTPS.

## Command breakdown

| Command | What it does |
|---|---|
| `git remote set-url origin git@github.com:O/R.git` | HTTPS → SSH for one clone |
| `git config --global url."git@github.com:".insteadOf https://github.com/` | rewrite for every clone |
| `ssh -T -p 443 git@ssh.github.com` | test SSH over port 443 |
| `Host github.com` / `Hostname ssh.github.com` / `Port 443` | make that permanent in `~/.ssh/config` |

## Hands-on exercise

**Instructions.** Switch `origin` back to HTTPS and verify Git can read it.

**Expected result.** `git ls-remote origin` lists `refs/heads/master`.

<!-- test-run: cd ~/git-practice/lesson-50 && git remote set-url origin https://github.com/octocat/Hello-World.git -->

**Verification.**

<!-- test: contains=refs/heads/master -->
```bash
cd ~/git-practice/lesson-50
git ls-remote origin
```

## Break it

A network where outgoing port 22 is blocked (hotel, corporate proxy). Simulated by pointing ssh at a port nothing
answers on, with a short timeout:

<!-- test: fail; contains=Connection; output -->
```bash
ssh -o ConnectTimeout=5 -p 2 -T git@github.com 2>&1
```

```text
ssh: connect to host github.com port 2: Connection timed out
```

## Troubleshoot

`Connection timed out` / `Connection refused` comes **before** any authentication: it is a network problem, not a key
problem (compare with `Permission denied (publickey)` in lesson 49, which means the network worked). GitHub offers SSH
on port 443 too, at the host `ssh.github.com`:

<!-- test: fail; contains=Permission denied (publickey); output -->
```bash
ssh-keyscan -t ed25519 -p 443 ssh.github.com 2> /dev/null >> ~/.ssh/known_hosts
ssh -T -p 443 git@ssh.github.com 2>&1
```

```text
git@ssh.github.com: Permission denied (publickey).
```

`Permission denied (publickey)` here is good news: port 443 reached GitHub's SSH server (this lab has no registered
key, lesson 49).

## Fix

Make port 443 permanent for github.com, so the normal URLs keep working:

<!-- test: contains=port 443; contains=hostname ssh.github.com; output -->
```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
  Hostname ssh.github.com
  Port 443
  User git
EOF
ssh -G github.com | grep -E "^hostname|^port"
```

```text
Pseudo-terminal will not be allocated because stdin is not a terminal.
hostname ssh.github.com
port 443
```

## Real-world example

A team standardises on HTTPS + Git Credential Manager on laptops (works behind every proxy, tokens expire, SSO
enforced), and on read-only deploy keys or GitHub App tokens for servers. Another team uses SSH keys on hardware
security keys (`ssh-keygen -t ed25519-sk`). Both are fine; what hurts is a mix nobody understands, with keys from people
who left years ago still registered.

## Practice challenge

Write a one-liner that tells you whether the current clone uses SSH or HTTPS.

<details>
<summary>Solution</summary>

<!-- test: contains=HTTPS; output -->
```bash
cd ~/git-practice/lesson-50
case "$(git remote get-url origin)" in https://*) echo HTTPS ;; git@*|ssh://*) echo SSH ;; *) echo other ;; esac
```

```text
HTTPS
```

</details>

## Recap

- Same repository, two transports: HTTPS (port 443, tokens) and SSH (port 22 or 443, keys).
- `git remote set-url` or `url.<base>.insteadOf` switch between them.
- Timeouts = network; `Permission denied (publickey)` = authentication.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-50
```

Next: [Module 11 · Lesson 51 · What is a pull request?](../../11-pull-requests/51-what-is-pull-request/README.md).
