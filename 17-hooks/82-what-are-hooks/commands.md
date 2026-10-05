<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 82 · What are Git hooks? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-82 basic
cd ~/git-practice/lesson-82
```

## Demonstration

```bash
ls .git/hooks
```

```bash
cat > .git/hooks/post-commit << 'EOF'
#!/bin/sh
# post-commit: record every commit in a local log
echo "$(git log -1 --format='%h %s')" >> .git/commit-log.txt
EOF
chmod +x .git/hooks/post-commit
ls .git/hooks | grep -v sample
```

```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
cat .git/commit-log.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-82
wc -l < .git/commit-log.txt
```

## Break it

```bash
cat > .git/hooks/pre-commit.sh << 'EOF'
#!/bin/sh
if git diff --cached | grep -q "^+.*TODO"; then echo "pre-commit: remove the TODO first"; exit 1; fi
EOF
chmod +x .git/hooks/pre-commit.sh
echo "TODO: add prices for tea" >> menu.txt && git commit -q -am "Add a TODO" && git log --oneline -1
```

## Troubleshoot

```bash
git hook run pre-commit 2>&1
```

## Fix

```bash
mv .git/hooks/pre-commit.sh .git/hooks/pre-commit
git reset -q --soft HEAD~1
git commit -m "Add a TODO" 2>&1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-82
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
if awk 'NF < 2' prices.txt | grep -q .; then echo "pre-push: a menu item has no price"; exit 1; fi
EOF
chmod +x .git/hooks/pre-push
echo "mocha" >> prices.txt
git hook run pre-push 2>&1 || true
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-82
```
