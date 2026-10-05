# Lesson 89 · Secrets in Git

> Level 19 · Git security · ⏱ 25 minutes

## What are we learning?

Why a password, API token or access key in a Git repository is a serious incident: Git remembers every version, every
clone has a full copy, and deleting the file in a new commit does **not** remove it. We commit a (fake) secret, try to
"delete" it, find it again, and set up the habits that prevent it.

## Visual

```text
 commit 1   add .env (DB_PASSWORD=…, API_TOKEN=…)      ← the secret is now in a blob
 commit 2   git rm .env  "remove secrets"               ← the latest snapshot has no .env …
                                                          … but commit 1 still has it, in every clone,
                                                          in forks, CI caches, and on GitHub

 Rule: a secret that reached a shared repository is COMPROMISED → revoke/rotate it first, clean history second.
```

Typical secrets: `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`, `PASSWORD`, `API_TOKEN`, private keys (`id_rsa`,
`*.pem`), `.env` files, kubeconfigs, Terraform state.

## Lab setup

<!-- test: contains=lesson-89 -->
```bash
bash scripts/new-lab.sh lesson-89 remote
cd ~/git-practice/lesson-89/ada
```

## Demonstration

Ada adds the app configuration, secrets included (all values here are fake), and pushes:

<!-- test: contains=main -> main; output -->
```bash
printf 'DB_HOST=db.internal\nDB_PASSWORD=Cafe-2026-not-a-real-password\nAPI_TOKEN=cafe_token_0123456789abcdef\n' > .env
git add .env && git commit -q -m "Add app configuration"
git push 2>&1 | tail -1
```

```text
   4267004..a8b2304  main -> main
```

She notices and "removes" it:

<!-- test: contains=main -> main; output -->
```bash
git rm -q .env && git commit -q -m "Remove secrets" && git push 2>&1 | tail -1
ls -a | grep -c "^.env$" || true
```

```text
   a8b2304..7b0796b  main -> main
0
```

Someone else clones the repository later (a new clone, `eve`). The file is not in the folder, but it is in the
history:

<!-- test: contains=DB_PASSWORD; output -->
```bash
cd .. && git clone -q server/cafe.git eve && cd eve
git log --oneline -- .env
git show HEAD~1:.env
```

```text
7b0796b (HEAD -> main, origin/main, origin/HEAD) Remove secrets
a8b2304 Add app configuration
DB_HOST=db.internal
DB_PASSWORD=Cafe-2026-not-a-real-password
API_TOKEN=cafe_token_0123456789abcdef
```

Anyone with read access, now or in the future, can do this.

## Command breakdown

| Command | Finds |
|---|---|
| `git log --all -- FILE` | every commit that touched FILE, even deleted |
| `git log -p -S "TEXT" --all` | commits that added or removed TEXT |
| `git grep "PATTERN" $(git rev-list --all)` | PATTERN in every version of every file |
| `gitleaks detect` / `trufflehog git file://.` | dedicated scanners for many secret formats, whole history |

## Hands-on exercise

**Instructions.** Search the entire history of the clone for anything that looks like a password assignment.

**Expected result.** The commit and line containing `DB_PASSWORD=`.

**Verification.**

<!-- test: contains=DB_PASSWORD -->
```bash
cd ~/git-practice/lesson-89/eve
git grep -n "PASSWORD=" $(git rev-list --all) | head -3
```

## Break it

Believing `git rm` was enough, nobody rotates the password, and the repository is made public / forked / cloned by a
contractor. The secret has left your control; there is no command that "un-shares" it.

<!-- test: contains=still readable; output -->
```bash
git log --all --format=%h -- .env | while read -r c; do git show "$c:.env" 2> /dev/null | grep -q PASSWORD && echo "$c: password still readable"; done
```

```text
a8b2304: password still readable
```

## Troubleshoot

Ask, in this order:

1. **Was it pushed?** Not pushed: amend/reset locally (lesson 83's fix) and you are done.
2. **Pushed: treat it as leaked.** Revoke or rotate the credential at its source (database, cloud console, API
   provider) **now**. This is the actual fix; it makes the leaked value worthless.
3. Check the access logs of that system for use of the credential since the push.
4. Then clean the history (lesson 90), so the old value stops triggering alarms and does not spread further.

## Fix

The repository side of the fix, after rotation: keep configuration with secrets out of Git for good, and commit a
template instead.

<!-- test: contains=.env.example; output -->
```bash
cd ~/git-practice/lesson-89/ada
printf 'DB_HOST=db.internal\nDB_PASSWORD=\nAPI_TOKEN=\n' > .env.example
echo ".env" >> .gitignore
git add .env.example .gitignore && git commit -q -m "Add .env.example; ignore .env"
git ls-files
```

```text
.env.example
.gitignore
README.md
menu.txt
prices.txt
```

Real values then come from the environment, a secret manager (AWS Secrets Manager, Vault, Kubernetes Secrets via an
operator), or CI secrets: never from the repository.

## Real-world example

Public GitHub repositories are scanned by bots within minutes of a push; leaked cloud keys are typically abused for
crypto-mining almost immediately. GitHub's **secret scanning** and **push protection** block many known token formats
at push time, and cloud providers revoke some leaked keys automatically, but neither replaces rotation and
prevention: `.gitignore`, pre-commit scanners (lesson 83), short-lived credentials (OIDC from CI to the cloud
instead of stored keys).

## Practice challenge

Find the commit that **introduced** the token, by its value, with the pickaxe search.

<details>
<summary>Solution</summary>

<!-- test: contains=Add app configuration; output -->
```bash
cd ~/git-practice/lesson-89/eve
git log --oneline -S "cafe_token_" --all
```

```text
7b0796b (HEAD -> main, origin/main, origin/HEAD) Remove secrets
a8b2304 Add app configuration
```

`-S` lists commits where the number of occurrences changed: the one that added it and the one that removed it.

</details>

## Recap

- Deleting a secret in a new commit does not remove it from history or from clones.
- A pushed secret is compromised: rotate it first, then clean history.
- Prevent: `.gitignore`, `.env.example`, secret managers, pre-commit and server-side scanning.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-89
```

Next: [Lesson 90 · Removing sensitive data](../90-removing-sensitive-data/README.md).
