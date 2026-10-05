<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 49 · SSH authentication · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Test the connection before registering the key:

```bash
ssh -T git@github.com 2>&1
```

```text
git@github.com: Permission denied (publickey).
```

## Troubleshoot

`Permission denied (publickey)`: the network and GitHub's host key are fine (we reached GitHub and it answered), but no
key ssh offered is registered on any account. The debug log shows which keys were offered:

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

```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "git-course lesson 49"
ssh -T git@github.com 2>&1
```

```text
```

`gh ssh-key add` needs the `admin:public_key` permission: `gh auth refresh -h github.com -s admin:public_key`.
GitHub answers `Hi YOUR-ACCOUNT! You've successfully authenticated, but GitHub does not provide shell access.` (`ssh -T`
exits with status 1 even on success, because no shell is started.)
