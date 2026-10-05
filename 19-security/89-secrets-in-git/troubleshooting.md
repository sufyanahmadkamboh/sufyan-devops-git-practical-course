<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 89 · Secrets in Git · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Believing `git rm` was enough, nobody rotates the password, and the repository is made public / forked / cloned by a
contractor. The secret has left your control; there is no command that "un-shares" it.

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
