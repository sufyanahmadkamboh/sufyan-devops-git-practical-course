# Problem 12 · Accidentally committed secret

> Troubleshooting lab · run every command from the course folder · related lessons: [89](../19-security/89-secrets-in-git/README.md), [90](../19-security/90-removing-sensitive-data/README.md), [83](../17-hooks/83-pre-commit-hook/README.md)

## Problem

A database password went into a commit, and the commit was pushed. (All values in this lab are fake.)

<!-- test: contains=lesson-t12 -->
```bash
bash scripts/new-lab.sh lesson-t12 remote
cd ~/git-practice/lesson-t12/ada
printf 'db_host: db.internal\ndb_password: Cafe-2026-not-a-real-password\n' > config.yml
git add config.yml && git commit -q -m "Add config" && git push -q
```

## Symptoms

A teammate, a scanner, or GitHub's secret scanning reports a credential in the repository.

<!-- test: contains=db_password; output -->
```bash
git grep -n "password" $(git rev-list --all) | sed -E 's/(password: ).*/\1…/'
```

```text
003a5aa4a77576d226d58c49808e3a2dcd24ec5c:config.yml:2:db_password: …
```

## Investigation

Which commits contain it, is it pushed, and where else could it be?

<!-- test: contains=Add config; output -->
```bash
git log --oneline -S "Cafe-2026-not-a-real-password" --all
git branch -r --contains "$(git log --format=%h -1 -S Cafe-2026-not-a-real-password)"
```

```text
003a5aa (HEAD -> main, origin/main, origin/HEAD) Add config
  origin/HEAD -> origin/main
  origin/main
```

## Commands

| Command | Shows |
|---|---|
| `git log -S "VALUE" --all` | commits that added/removed the value |
| `git branch -r --contains SHA` | which remote branches have that commit (= pushed) |
| `gitleaks detect` / `trufflehog git` | scanners for the whole history |

## Understand the output

"Add config" introduced the password, and `origin/main` contains it: the secret is on the server and in every clone
made since. Treat it as known by others.

## Root cause

A configuration file with a real credential was committed; nothing (`.gitignore`, pre-commit scanner, push
protection) stopped it.

## Fix

1. **Rotate the credential now** (change the database password at the source). This is the real fix.
2. Remove the value from the files and keep it out:

<!-- test: contains=DB_PASSWORD; output -->
```bash
printf 'db_host: db.internal\ndb_password: ${DB_PASSWORD}\n' > config.yml
git commit -q -am "Read the database password from the environment" && git push -q
cat config.yml
```

```text
db_host: db.internal
db_password: ${DB_PASSWORD}
```

3. Remove it from history (lesson 90), on a mirror clone, then force-push and have everyone re-clone:

<!-- test: contains=0; output -->
```bash
cd ~/git-practice/lesson-t12
git clone -q --mirror server/cafe.git cleanup.git && cd cleanup.git
echo 'Cafe-2026-not-a-real-password==>***REMOVED***' > ../replacements.txt
git filter-repo --replace-text ../replacements.txt > /dev/null 2>&1
git push -q --force --mirror ../server/cafe.git 2> /dev/null
git --git-dir=../server/cafe.git log --all -p | grep -c "Cafe-2026" || true
```

```text
0
```

## Verification

<!-- test: contains=REMOVED; output -->
```bash
cd ~/git-practice/lesson-t12 && rm -rf ada && git clone -q server/cafe.git ada
git -C ada log --all -p | grep "db_password" | sort -u
```

```text
+db_password: ${DB_PASSWORD}
+db_password: ***REMOVED***
-db_password: ***REMOVED***
```

## Prevention

- `.gitignore` for configuration with secrets; commit templates (`config.example.yml`).
- A pre-commit secret scanner (lesson 83) and GitHub push protection.
- Short-lived credentials (OIDC from CI, a secret manager) so a leak expires on its own.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t12
```

Next: [Problem 13 · Large file rejected](problem-13-large-file-rejected.md)
