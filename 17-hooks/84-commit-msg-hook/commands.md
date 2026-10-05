<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 84 · Commit message hook · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-84 basic
cd ~/git-practice/lesson-84
```

## Demonstration

```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/usr/bin/env bash
# commit-msg: require Conventional Commits, e.g. "feat(menu): add green tea"
subject=$(head -n 1 "$1")
case "$subject" in Merge*|Revert*|fixup!*|squash!*) exit 0 ;; esac
pattern='^(feat|fix|docs|chore|refactor|test|ci|build|perf)(\([a-z0-9-]+\))?!?: .{1,72}$'
if ! echo "$subject" | grep -Eq "$pattern"; then
  echo "commit-msg: \"$subject\" does not follow Conventional Commits"
  echo "  expected: type(scope): description   e.g. feat(menu): add green tea"
  exit 1
fi
EOF
chmod +x .git/hooks/commit-msg
ls .git/hooks | grep -v sample
```

```bash
echo "green tea" >> menu.txt && git commit -q -am "feat(menu): add green tea"
git log --oneline -1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-84
git log --oneline -1
```

## Break it

```bash
echo "mocha" >> menu.txt
git commit -am "fixed stuff" 2>&1
```

## Troubleshoot

```bash
git status --short
```

## Fix

```bash
git commit -q -am "feat(menu): add mocha"
git log --oneline -1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-84
git log --format=%s 4267004..HEAD | sed -E 's/^([a-z]+).*/\1/' | sort | uniq -c
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-84
```
