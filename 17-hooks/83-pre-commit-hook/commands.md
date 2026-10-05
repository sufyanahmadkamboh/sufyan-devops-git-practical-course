<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 83 · Pre-commit hook · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-83 basic
cd ~/git-practice/lesson-83
```

## Demonstration

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
# pre-commit: block secrets and large files in the staged changes
status=0
added=$(git diff --cached --no-color -U0 | grep '^+' | grep -v '^+++')
if echo "$added" | grep -Eq 'AKIA[0-9A-Z]{16}'; then
  echo "pre-commit: an AWS access key ID is staged"; status=1
fi
if echo "$added" | grep -q -- '-----BEGIN [A-Z ]*PRIVATE KEY-----'; then
  echo "pre-commit: a private key is staged"; status=1
fi
while IFS= read -r f; do
  [ -f "$f" ] && [ "$(wc -c < "$f")" -gt 1048576 ] && { echo "pre-commit: $f is larger than 1 MB (use Git LFS, lesson 88)"; status=1; }
done < <(git diff --cached --name-only --diff-filter=AM)
[ $status -eq 0 ] || echo "commit blocked: fix the files above (or unstage them)"
exit $status
EOF
chmod +x .git/hooks/pre-commit
ls .git/hooks | grep -v sample
```

```bash
echo "green tea" >> menu.txt && git commit -am "Add green tea"
```

```bash
printf 'aws_access_key_id = AKIA%s\n' "IOSFODNN7EXAMPLE" > config.ini
git add config.ini
git commit -m "Add the config" 2>&1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-83
git log --oneline -1
git show HEAD:config.ini
```

## Break it

```bash
printf 'debug_key = AKIA%s\n' "IOSFODNN7EXAMPLE" > debug.ini
git add debug.ini
git commit -q --no-verify -m "Add debug settings"
git log --oneline -1
```

## Troubleshoot

```bash
git show HEAD --stat --format=%s
git show HEAD:debug.ini | sed -E 's/(AKIA....).*/\1…/'
```

## Fix

```bash
git reset -q --soft HEAD~1
git restore --staged debug.ini && rm debug.ini
echo "debug.ini" >> .gitignore && git add .gitignore && git commit -q -m "Ignore debug.ini"
git log --oneline -1
git ls-files | grep -x debug.ini || echo "debug.ini is not tracked"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-83
head -c 2097152 /dev/zero > big.bin && git add big.bin
git hook run pre-commit 2>&1 || true
git restore --staged big.bin && rm big.bin
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-83
```
