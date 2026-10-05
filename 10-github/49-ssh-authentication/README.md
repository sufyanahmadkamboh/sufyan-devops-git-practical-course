# Lesson 49 · SSH authentication

> Level 10 · Authentication · ⏱ 25 minutes

## What are we learning?

How to authenticate to GitHub with an SSH key pair: create the key with `ssh-keygen`, trust GitHub's host key, add the
public key to your account, and verify with `ssh -T git@github.com`.

## Visual

```text
 your computer                                   GitHub
 ~/.ssh/id_ed25519      (PRIVATE: never leaves)
 ~/.ssh/id_ed25519.pub  (public) ──── added once to Settings → SSH and GPG keys
 ~/.ssh/known_hosts     GitHub's host key ◄─── checked on every connection: "am I talking to the real GitHub?"

 ssh -T git@github.com
   1. GitHub proves its identity (host key, compared with known_hosts)
   2. you prove yours: a signature made with the private key, checked against your registered public key
   3. "Hi YOU! You've successfully authenticated, but GitHub does not provide shell access."
```

## Lab setup

<!-- test: contains=lesson-49 -->
```bash
bash scripts/new-lab.sh lesson-49 empty
cd ~/git-practice/lesson-49
ls ~/.ssh 2>/dev/null || echo "no ~/.ssh yet"
```

## Demonstration

**1. Create a key pair.** Ed25519 is the modern default. On your computer, give it a passphrase when asked (here `-N ""`
creates one without, so the lesson runs unattended):

<!-- test: contains=id_ed25519.pub; output -->
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_ed25519 -N ""
ls ~/.ssh
ssh-keygen -l -f ~/.ssh/id_ed25519.pub | awk '{print $1, $3, $4}'
```

```text
id_ed25519
id_ed25519.pub
256 ada@example.com (ED25519)
```

The `.pub` file is the part you share; `id_ed25519` is the secret.

**2. Trust GitHub's host key.** On the first connection ssh shows a fingerprint and asks "Are you sure you want to
continue connecting?". Compare it with the fingerprints GitHub publishes (docs: "GitHub's SSH key fingerprints", or
`gh api meta`) instead of answering "yes" blindly:

<!-- test: contains=+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU; output -->
```bash
ssh-keyscan -t ed25519 github.com 2> /dev/null >> ~/.ssh/known_hosts
ssh-keygen -l -f ~/.ssh/known_hosts
```

```text
256 SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU github.com (ED25519)
```

`SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` is GitHub's published ED25519 fingerprint: the host is genuine.

## Command breakdown

| Command | What it does |
|---|---|
| `ssh-keygen -t ed25519 -C "email"` | create a key pair (asks for file and passphrase) |
| `ssh-keygen -l -f FILE` | show a key's fingerprint |
| `ssh-add ~/.ssh/id_ed25519` | load the key into the agent (passphrase typed once per session) |
| `gh ssh-key add FILE.pub --title NAME` | register the public key on GitHub (or: Settings → SSH and GPG keys) |
| `ssh -T git@github.com` | test: who does GitHub think I am? |
| `ssh -vT git@github.com` | the same, with a debug log of every step |

## Hands-on exercise

**Instructions.** Print your public key, the text you would paste into GitHub's "New SSH key" form.

**Expected result.** One line starting with `ssh-ed25519` and ending with your comment.

**Verification.**

<!-- test: contains=ssh-ed25519; contains=ada@example.com -->
```bash
cat ~/.ssh/id_ed25519.pub
```

## Break it

Test the connection before registering the key:

<!-- test: fail; contains=Permission denied (publickey); output -->
```bash
ssh -T git@github.com 2>&1
```

```text
git@github.com: Permission denied (publickey).
```

## Troubleshoot

`Permission denied (publickey)`: the network and GitHub's host key are fine (we reached GitHub and it answered), but no
key ssh offered is registered on any account. The debug log shows which keys were offered:

<!-- test: contains=Offering public key; output -->
```bash
ssh -vT git@github.com 2>&1 | grep -E "Offering public key|Authentications that can continue|Permission denied"
```

```text
debug1: Authentications that can continue: publickey
debug1: Offering public key: ~/.ssh/id_ed25519 ED25519 SHA256:9C94jYMDra8ABvS7yDuhlN1VINlbwjMWac3wC+1u6xQ
debug1: Authentications that can continue: publickey
git@github.com: Permission denied (publickey).
```

Typical causes: the key is not added to GitHub; it was added to a **different account**; ssh offers another key
(several keys, wrong `IdentityFile` in `~/.ssh/config`); the private key file has too-open permissions (ssh then
refuses to use it).

## Fix

Register the public key with your account (web: Settings → SSH and GPG keys → New SSH key, paste the `.pub` line):

<!-- test: skip; output -->
```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "git-course lesson 49"
ssh -T git@github.com 2>&1
```

```text
```

`gh ssh-key add` needs the `admin:public_key` permission: `gh auth refresh -h github.com -s admin:public_key`.
GitHub answers `Hi YOUR-ACCOUNT! You've successfully authenticated, but GitHub does not provide shell access.` (`ssh -T`
exits with status 1 even on success, because no shell is started.)

## Real-world example

Servers and CI runners that must clone one private repository use a **deploy key**: an SSH key registered on that
single repository (repository → Settings → Deploy keys), read-only by default. Unlike a personal key, it gives no
access to anything else, and removing it does not affect any person's account.

## Practice challenge

Use different keys for two GitHub accounts (personal and work) on the same computer, with `~/.ssh/config` host
aliases. Show which key each alias would use.

<details>
<summary>Solution</summary>

<!-- test: contains=id_work; output -->
```bash
ssh-keygen -q -t ed25519 -C "ada@work.example.com" -f ~/.ssh/id_work -N ""
cat >> ~/.ssh/config << 'EOF'
Host github.com
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_work
  IdentitiesOnly yes
EOF
ssh -G github-work | grep -E "^hostname|^identityfile" | sed "s|$HOME|~|"
```

```text
Pseudo-terminal will not be allocated because stdin is not a terminal.
hostname github.com
identityfile ~/.ssh/id_work
```

A work repository is then cloned as `git clone git@github-work:company/repo.git`: ssh connects to github.com with the
work key.

</details>

## Recap

- `ssh-keygen -t ed25519` creates the pair; only the `.pub` part goes to GitHub.
- Verify GitHub's host key fingerprint once; `known_hosts` remembers it.
- `ssh -T git@github.com` tests; `Permission denied (publickey)` = no registered key was offered.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-49
```

Keep `~/.ssh`; if you registered the key only for this lesson, remove it on GitHub (Settings → SSH and GPG keys, or
`gh ssh-key delete`).

Next: [Lesson 50 · SSH vs HTTPS](../50-ssh-vs-https/README.md).
