<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 49 · SSH authentication · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-49 empty
cd ~/git-practice/lesson-49
ls ~/.ssh 2>/dev/null || echo "no ~/.ssh yet"
```

## Demonstration

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_ed25519 -N ""
ls ~/.ssh
ssh-keygen -l -f ~/.ssh/id_ed25519.pub | awk '{print $1, $3, $4}'
```

```bash
ssh-keyscan -t ed25519 github.com 2> /dev/null >> ~/.ssh/known_hosts
ssh-keygen -l -f ~/.ssh/known_hosts
```

## Hands-on exercise

```bash
cat ~/.ssh/id_ed25519.pub
```

## Break it

```bash
ssh -T git@github.com 2>&1
```

## Troubleshoot

```bash
ssh -vT git@github.com 2>&1 | grep -E "Offering public key|Authentications that can continue|Permission denied"
```

## Fix

```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "git-course lesson 49"
ssh -T git@github.com 2>&1
```

## Practice challenge

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

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-49
```
