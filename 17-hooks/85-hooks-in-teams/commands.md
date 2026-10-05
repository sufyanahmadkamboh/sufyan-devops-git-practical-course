<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 85 · Git hooks in teams · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-85 remote
cd ~/git-practice/lesson-85/ada
```

## Demonstration

```bash
mkdir -p .githooks
cat > .githooks/commit-msg << 'EOF'
#!/usr/bin/env bash
# commit-msg: require a type prefix such as "feat:" or "fix:"
head -n 1 "$1" | grep -Eq '^(Merge|Revert|(feat|fix|docs|chore|refactor|test|ci)(\([a-z0-9-]+\))?!?: )' && exit 0
echo "commit-msg: start the message with a type, e.g. \"feat: add green tea\""; exit 1
EOF
chmod +x .githooks/commit-msg
git add .githooks && git commit -q -m "chore: add the team's Git hooks"
git push -q
git ls-files .githooks
```

```bash
git config core.hooksPath .githooks
echo "green tea" >> menu.txt && git commit -am "green tea" 2>&1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-85
git --git-dir=server/cafe.git log --oneline -1
```

## Break it

```bash
cd ~/git-practice/lesson-85/grace && git pull -q
ls .githooks
echo "mocha" >> menu.txt && git commit -q -am "whatever" && git log --oneline -1
```

## Troubleshoot

```bash
git config core.hooksPath || echo "core.hooksPath not set in Grace's clone"
```

## Fix

```bash
git config core.hooksPath .githooks
git commit -q --amend -m "feat: add mocha"
git log --oneline -1
```

```bash
git log --format=%s origin/main..HEAD | grep -Ev '^(Merge|(feat|fix|docs|chore|refactor|test|ci)(\(.+\))?!?: )' && exit 1 || echo "all commit messages follow the convention"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-85/grace
git rev-parse --git-path hooks/commit-msg
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-85
```
