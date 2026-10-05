<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 73 · .gitignore · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-73 basic
cd ~/git-practice/lesson-73
mkdir -p node_modules/left-pad logs
echo "module" > node_modules/left-pad/index.js
echo "error" > logs/error.log && echo "keep" > keep.log
echo "API_TOKEN=local-secret" > .env
git status --short
```

## Demonstration

```bash
printf 'node_modules/\n.env\n*.log\n!keep.log\n' > .gitignore
git status --short
```

```bash
git check-ignore -v logs/error.log .env node_modules/left-pad/index.js
git check-ignore -v keep.log || echo "keep.log is not ignored"
```

```bash
git add .
git commit -m "Add .gitignore and keep.log"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-73
git check-ignore -v .vscode/settings.json
```

## Break it

```bash
echo "debug=false" > config.local && git add config.local && git commit -q -m "Add config"
echo "config.local" >> .gitignore && git commit -q -am "Ignore config.local"
echo "debug=true" > config.local
git status --short
```

## Troubleshoot

```bash
git ls-files | grep config
```

## Fix

```bash
git rm -q --cached config.local
git commit -q -m "Stop tracking config.local"
git status --short --ignored | grep config
cat config.local
```

## Practice challenge

```bash
cd ~/git-practice/lesson-73
echo "Application logs are written here." > logs/README.md
printf 'logs/*\n!logs/README.md\n' >> .gitignore
git add . && git commit -q -m "Keep logs/README.md"
git ls-files logs
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-73
```
