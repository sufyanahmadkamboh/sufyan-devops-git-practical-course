# Lesson 83 · Pre-commit hook

> Level 17 · Git hooks · ⏱ 25 minutes

## What are we learning?

A practical `pre-commit` hook that checks the **staged** changes before every commit: it blocks AWS-style access keys,
private keys and files over 1 MB. And why a local hook is a convenience, not a security control.

## Visual

```text
 git commit
    │
    ▼
 .git/hooks/pre-commit   reads: git diff --cached (exactly what will be committed)
    ├── AKIA… access key?          → exit 1: "commit blocked"
    ├── -----BEGIN … PRIVATE KEY   → exit 1
    ├── file > 1 MB?               → exit 1
    └── all fine                   → exit 0 → commit created
```

## Lab setup

<!-- test: contains=lesson-83 -->
```bash
bash scripts/new-lab.sh lesson-83 basic
cd ~/git-practice/lesson-83
```

## Demonstration

The hook:

<!-- test: contains=pre-commit -->
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

A normal change passes:

<!-- test: contains=1 file changed -->
```bash
echo "green tea" >> menu.txt && git commit -am "Add green tea"
```

A configuration file with a credential does not. (The key is AWS's documentation example, built in two parts so this
course itself never contains the full pattern.)

<!-- test: fail; contains=an AWS access key ID is staged; output -->
```bash
printf 'aws_access_key_id = AKIA%s\n' "IOSFODNN7EXAMPLE" > config.ini
git add config.ini
git commit -m "Add the config" 2>&1
```

```text
pre-commit: an AWS access key ID is staged
commit blocked: fix the files above (or unstage them)
```

## Command breakdown

| Command | Use in a hook |
|---|---|
| `git diff --cached` | the staged changes (what will be committed) |
| `git diff --cached --name-only --diff-filter=AM` | added or modified staged files |
| `git hook run pre-commit` | test the hook without committing |
| `git commit --no-verify` (`-n`) | skip `pre-commit` and `commit-msg` |
| `gitleaks protect --staged` / `detect-secrets` | dedicated secret scanners to call from the hook |

## Hands-on exercise

**Instructions.** Replace the key with a reference to an environment variable and commit successfully.

**Expected result.** The hook passes; the commit contains no key.

<!-- test-run: cd ~/git-practice/lesson-83 && echo 'aws_access_key_id = ${AWS_ACCESS_KEY_ID}' > config.ini && git add config.ini && git commit -q -m "Add the config (key from the environment)" -->

**Verification.**

<!-- test: contains=AWS_ACCESS_KEY_ID; absent=IOSFODNN -->
```bash
cd ~/git-practice/lesson-83
git log --oneline -1
git show HEAD:config.ini
```

## Break it

In a hurry, someone bypasses the hook:

<!-- test: contains=Add debug settings; output -->
```bash
printf 'debug_key = AKIA%s\n' "IOSFODNN7EXAMPLE" > debug.ini
git add debug.ini
git commit -q --no-verify -m "Add debug settings"
git log --oneline -1
```

```text
a9c217c (HEAD -> main) Add debug settings
```

## Troubleshoot

`--no-verify` skips `pre-commit` entirely, and so does a fresh clone (hooks are not cloned), a GUI client configured
differently, or a commit made on another machine. The secret is now in a commit:

<!-- test: contains=AKIA; output -->
```bash
git show HEAD --stat --format=%s
git show HEAD:debug.ini | sed -E 's/(AKIA....).*/\1…/'
```

```text
Add debug settings

 debug.ini | 1 +
 1 file changed, 1 insertion(+)
debug_key = AKIAIOSF…
```

## Fix

Not pushed yet: remove the file from the commit and from Git's tracking, keep it ignored. (If it had been pushed, the
key must be **revoked** and history cleaned: lessons 89–90.)

<!-- test: contains=debug.ini is not tracked; output -->
```bash
git reset -q --soft HEAD~1
git restore --staged debug.ini && rm debug.ini
echo "debug.ini" >> .gitignore && git add .gitignore && git commit -q -m "Ignore debug.ini"
git log --oneline -1
git ls-files | grep -x debug.ini || echo "debug.ini is not tracked"
```

```text
3ed7a18 (HEAD -> main) Ignore debug.ini
debug.ini is not tracked
```

Prevention at the server: GitHub **push protection** (secret scanning) rejects pushes containing known key formats,
and CI runs the same scanner; neither can be skipped with `--no-verify`.

## Real-world example

The [pre-commit](https://pre-commit.com) framework manages hooks from a `.pre-commit-config.yaml` committed in the
repository: `gitleaks`, `terraform_fmt`, `check-added-large-files`, `end-of-file-fixer`. Developers run `pre-commit
install` once; CI runs `pre-commit run --all-files`, so the same checks protect the repository even when a local hook
was skipped.

## Practice challenge

Test the hook without committing: stage a 2 MB file and run the hook directly.

<details>
<summary>Solution</summary>

<!-- test: contains=larger than 1 MB; output -->
```bash
cd ~/git-practice/lesson-83
head -c 2097152 /dev/zero > big.bin && git add big.bin
git hook run pre-commit 2>&1 || true
git restore --staged big.bin && rm big.bin
```

```text
pre-commit: big.bin is larger than 1 MB (use Git LFS, lesson 88)
commit blocked: fix the files above (or unstage them)
```

</details>

## Recap

- `pre-commit` checks `git diff --cached`; exit 1 aborts the commit.
- Block secrets, private keys and large files early, with clear messages.
- Local hooks can be skipped: enforce the same checks in CI and with push protection.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-83
```

Next: [Lesson 84 · Commit message hook](../84-commit-msg-hook/README.md).
