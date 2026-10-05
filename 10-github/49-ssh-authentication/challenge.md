<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 49 · SSH authentication · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Use different keys for two GitHub accounts (personal and work) on the same computer, with `~/.ssh/config` host
aliases. Show which key each alias would use.

<details>
<summary>Solution</summary>

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
