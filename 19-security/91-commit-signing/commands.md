<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 91 · Commit signing · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-91 basic
cd ~/git-practice/lesson-91
mkdir -p ~/.ssh && chmod 700 ~/.ssh
[ -f ~/.ssh/id_signing ] || ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_signing -N ""
ls ~/.ssh | grep signing
```

## Demonstration

```bash
git config gpg.format ssh
git config user.signingkey "$HOME/.ssh/id_signing.pub"
git config --get gpg.format
```

```bash
echo "green tea" >> menu.txt && git commit -q -S -am "Add green tea"
git log --oneline -1
git cat-file -p HEAD | sed -n '/gpgsig/,/END SSH SIGNATURE/p' | head -3
```

```bash
echo "ada@example.com $(cat ~/.ssh/id_signing.pub)" > ~/.ssh/allowed_signers
git config gpg.ssh.allowedSignersFile "$HOME/.ssh/allowed_signers"
git verify-commit HEAD 2>&1 | sed "s|$HOME|~|"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-91
git log --format='%G? %h %s' -3
```

## Break it

```bash
git clone -q . ../lesson-91-teammate
git -C ../lesson-91-teammate verify-commit HEAD 2>&1
```

## Fix

```bash
mkdir -p .github && cp ~/.ssh/allowed_signers .github/allowed_signers
git add .github/allowed_signers && git commit -q -m "Add the team's allowed signers"
cd ../lesson-91-teammate && git pull -q
git config gpg.ssh.allowedSignersFile .github/allowed_signers
git verify-commit HEAD 2>&1 | sed "s|$HOME|~|"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-91
git tag -s v1.0.0 -m "Release 1.0.0"
git verify-tag v1.0.0 2>&1 | sed "s|$HOME|~|"
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-91 ~/git-practice/lesson-91-teammate
```
