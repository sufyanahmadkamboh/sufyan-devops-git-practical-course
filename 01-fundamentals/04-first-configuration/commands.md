<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 04 · First Git configuration · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-04 empty
cd ~/git-practice/lesson-04
```

## Demonstration

```bash
git config --global user.name "Ada Lovelace"
git config --global user.email "ada@example.com"
git config --global init.defaultBranch main
git config --global --list
```

```bash
git config --list --show-origin --show-scope | grep -E 'user\.|init\.'
```

```bash
git config user.email "ada@work.example.com"
git config --show-scope --get-all user.email
git config --show-scope --show-origin user.email
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-04
git config --show-scope --get user.email
```

## Break it

```bash
cd ~/git-practice/lesson-04
echo "test" > note.txt && git add note.txt
GIT_CONFIG_GLOBAL=/dev/null git -c user.useConfigOnly=true commit -m "First note" 2>&1
```

## Troubleshoot

```bash
GIT_CONFIG_GLOBAL=/dev/null git config --show-origin --get user.email || echo "no identity at any level"
```

## Fix

```bash
git config --global user.email >/dev/null && git commit -q -m "First note" && git log --format='%h %an <%ae> %s'
```

## Practice challenge

```bash
printf '[user]\n\temail = ada@work.example.com\n' > ~/.gitconfig-work
git config --global includeIf."gitdir:~/git-practice/work/".path '~/.gitconfig-work'
mkdir -p ~/git-practice/work/project && cd ~/git-practice/work/project && git init -q
git config --show-origin --get user.email
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-04 ~/git-practice/work ~/.gitconfig-work
git config --global --unset-all includeIf.gitdir:~/git-practice/work/.path || true
```
