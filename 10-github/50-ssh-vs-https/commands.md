<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 50 · SSH vs HTTPS · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-50 basic
cd ~/git-practice/lesson-50
git remote add origin https://github.com/octocat/Hello-World.git
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

## Demonstration

```bash
git remote set-url origin git@github.com:octocat/Hello-World.git
git remote -v
```

```bash
git remote set-url origin https://github.com/octocat/Hello-World.git
git config --global url."git@github.com:".insteadOf "https://github.com/"
git remote -v
git config --global --unset url."git@github.com:".insteadOf
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-50
git ls-remote origin
```

## Break it

```bash
ssh -o ConnectTimeout=5 -p 2 -T git@github.com 2>&1
```

## Troubleshoot

```bash
ssh-keyscan -t ed25519 -p 443 ssh.github.com 2> /dev/null >> ~/.ssh/known_hosts
ssh -T -p 443 git@ssh.github.com 2>&1
```

## Fix

```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
  Hostname ssh.github.com
  Port 443
  User git
EOF
ssh -G github.com | grep -E "^hostname|^port"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-50
case "$(git remote get-url origin)" in https://*) echo HTTPS ;; git@*|ssh://*) echo SSH ;; *) echo other ;; esac
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-50
```
