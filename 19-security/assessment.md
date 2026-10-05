# Module 19 · Git security · Assessment

> Lessons 89–92 · ⏱ 60 minutes · run every command from the course folder (`git-practical-course/`) · needs
> `git filter-repo` · all secrets in this assessment are fake

## Lab setup

The troubleshooting lab gets a fake AWS-style key in its history (built from two parts, so this course never contains
the full pattern):

<!-- test: contains=labs ready -->
```bash
bash scripts/new-lab.sh assess-19-practical basic
bash scripts/new-lab.sh assess-19-broken history
(cd ~/git-practice/assess-19-broken &&
  printf 'aws_access_key_id = AKIA%s\nregion = eu-central-1\n' "IOSFODNN7EXAMPLE" > deploy.conf &&
  git add deploy.conf && git commit -q -m "Add deploy settings" &&
  sed -i 's/^aws_access_key_id = .*/aws_access_key_id = ${AWS_ACCESS_KEY_ID}/' deploy.conf && git commit -q -am "Use the key from the environment")
mkdir -p ~/.ssh && chmod 700 ~/.ssh
[ -f ~/.ssh/id_assess19 ] || ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_assess19 -N ""
echo "labs ready"
```

## Quiz

1. A secret was removed in the next commit. Why is it still exposed?
2. What is the first thing to do when a secret reached a shared repository, before any history rewriting?
3. Which tool rewrites history to remove a file or a string, and why on a mirror clone?
4. After rewriting and force-pushing, why must every teammate re-clone?
5. What do the author name and email of a commit prove? What does a valid signature prove?
6. For SSH-signed commits, what does Git need to verify them, besides the signature?
7. Why pin a GitHub Action to a commit SHA rather than a tag like `@v4`?
8. Name two server-side controls that cannot be skipped with `--no-verify`.

<details>
<summary>Answers</summary>

1. Every earlier commit, every clone and fork keeps the version that contained it (lesson 89).
2. Revoke or rotate the credential at its source (lesson 89).
3. `git filter-repo` (`--invert-paths --path`, `--replace-text`); a mirror has all branches and tags and nothing else (lesson 90).
4. Old clones still hold the old history; their next push brings the secret back (lesson 90).
5. Author fields are free text, a claim; a valid signature proves possession of a private key trusted for that identity (lesson 91).
6. An allowed signers file (`gpg.ssh.allowedSignersFile`) mapping identities to trusted public keys (lesson 91).
7. Tags can be moved to other code; a full commit ID cannot change (lesson 92).
8. Branch protection (required reviews, required checks, signed commits), GitHub push protection / secret scanning, CI
   jobs required by protection (lessons 59, 89, 92).

</details>

## Practical challenge

In `~/git-practice/assess-19-practical`, with the SSH key `~/.ssh/id_assess19`:

1. Sign every new commit with that SSH key (configuration in this repository only).
2. Make a signed commit "Add chai" and a signed annotated tag `v1.0.0`.
3. Verification succeeds via an allowed signers file committed at `.github/allowed_signers`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Good "git" signature for ada@example.com; output -->
```bash
cd ~/git-practice/assess-19-practical
git config gpg.format ssh
git config user.signingkey "$HOME/.ssh/id_assess19.pub"
git config commit.gpgsign true
mkdir -p .github && echo "ada@example.com $(cat ~/.ssh/id_assess19.pub)" > .github/allowed_signers
git config gpg.ssh.allowedSignersFile .github/allowed_signers
git add .github && git commit -q -m "Add the allowed signers"
echo chai >> menu.txt && git commit -q -am "Add chai"
git tag -s v1.0.0 -m "Release 1.0.0"
git verify-commit HEAD 2>&1 | sed "s|$HOME|~|"
git verify-tag v1.0.0 2>&1 | sed "s|$HOME|~|"
```

```text
Good "git" signature for ada@example.com with ED25519 key SHA256:WgGJVyjXReY+XCWVH+0GYYoSRBbMoDkdJ6pmpwA1wEY
Good "git" signature for ada@example.com with ED25519 key SHA256:WgGJVyjXReY+XCWVH+0GYYoSRBbMoDkdJ6pmpwA1wEY
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-19-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "signing configured with SSH"      '[ "$(git config gpg.format)" = ssh ] && [ "$(git config commit.gpgsign)" = true ]'
check "allowed signers file committed"   'git ls-files --error-unmatch .github/allowed_signers'
check "Add chai has a good signature"    '[ "$(git log -1 --format=%G? --grep="^Add chai$")" = G ]'
check "v1.0.0 is a signed tag"           'git verify-tag v1.0.0'
```

```text
ok       signing configured with SSH
ok       allowed signers file committed
ok       Add chai has a good signature
ok       v1.0.0 is a signed tag
```

## Troubleshooting challenge

A scanner reports an AWS access key ID in `~/git-practice/assess-19-broken`, although `deploy.conf` reads the key
from the environment now:

<!-- test: contains=AKIA; output -->
```bash
cd ~/git-practice/assess-19-broken
cat deploy.conf
git grep -n "AKIA" $(git rev-list --all) | sed -E 's/(AKIA)[A-Z0-9]+/\1…/'
```

```text
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
region = eu-central-1
02a6f096000fbae98c4e136adab1737ad30e1443:deploy.conf:1:aws_access_key_id = AKIA…
```

Nothing has been pushed. The key has been rotated (assume so). Remove it from the history.

<details>
<summary>Solution</summary>

The value is still in the commit "Add deploy settings". Replace it everywhere in history with `git filter-repo`
(`--force`: this is a working clone, not a fresh mirror; acceptable here because nothing is shared):

<!-- test: contains=REMOVED; output -->
```bash
printf 'regex:AKIA[A-Z0-9]{16}==>***REMOVED***\n' > ../assess-19-replacements.txt
git filter-repo --force --replace-text ../assess-19-replacements.txt > /dev/null 2>&1
git show HEAD~1:deploy.conf
```

```text
aws_access_key_id = ***REMOVED***
region = eu-central-1
```

The replacement rule itself is a regular expression, so the key never has to be written down again.

</details>

Verification:

<!-- test: contains=0; output -->
```bash
cd ~/git-practice/assess-19-broken
git grep "AKIA" $(git rev-list --all) | wc -l
git log --oneline -3
```

```text
0
898accb (HEAD -> main) Use the key from the environment
f63776c Add deploy settings
ecff18a Price mocha
```

## Real-world scenario

A popular open-source GitHub Action you use as `uses: some-org/deploy@v2` is announced as compromised: for six
hours, `v2` pointed to a commit that printed environment variables to the logs. Your workflow ran three times in that
window. What do you do now, and what do you change?

<details>
<summary>Model answer</summary>

Now: treat every secret available to those workflow runs as leaked: rotate them (cloud keys, tokens, registry
credentials); check the run logs (and delete them), and audit cloud and registry activity since then. Change: pin
every third-party action to a full commit SHA (with the tag as a comment), let Dependabot/Renovate propose updates via
PRs, set least-privilege `permissions:` per workflow, replace long-lived secrets with OIDC short-lived credentials,
and restrict which actions may run in the organisation settings (lesson 92).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-19-practical ~/git-practice/assess-19-broken ~/git-practice/assess-19-replacements.txt ~/.ssh/id_assess19 ~/.ssh/id_assess19.pub
```
