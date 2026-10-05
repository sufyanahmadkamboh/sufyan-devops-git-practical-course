<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 50 · SSH vs HTTPS · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A network where outgoing port 22 is blocked (hotel, corporate proxy). Simulated by pointing ssh at a port nothing
answers on, with a short timeout:

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
