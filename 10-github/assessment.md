# Module 10 · GitHub and authentication · Assessment

> Lessons 44–50 · ⏱ 40 minutes · run every command from the course folder (`git-practical-course/`) · needs internet
> access, no GitHub account (nothing is created on GitHub)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-10-practical basic
bash scripts/new-lab.sh assess-10-broken basic
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

## Quiz

1. Which parts of a GitHub repository are stored in Git, and which only on GitHub?
2. Why does `git push` over HTTPS fail when you type your GitHub account password?
3. What does a credential helper do?
4. Which half of an SSH key pair goes to GitHub?
5. `ssh -T git@github.com` answers `Permission denied (publickey)`. Is the network the problem?
6. How do you switch an existing clone from HTTPS to SSH?
7. Your firewall blocks port 22. How can you still use SSH with GitHub?
8. A public repository URL asks you for a username. What is the most likely cause?

<details>
<summary>Answers</summary>

1. Code, commits, branches, tags are Git; issues, PRs, Actions, releases and settings are GitHub (lesson 47).
2. GitHub accepts only tokens for Git over HTTPS (lesson 48).
3. Stores a token and hands it to Git, so you are not asked (Git Credential Manager, `gh auth setup-git`) (lesson 48).
4. The public key, the `.pub` file (lesson 49).
5. No: the connection worked; no offered key is registered (lesson 49).
6. `git remote set-url origin git@github.com:OWNER/REPO.git` (lesson 50).
7. Use `ssh.github.com` on port 443, e.g. in `~/.ssh/config` (lesson 50).
8. A wrong owner or repository name, or a private repository you cannot access (lesson 44).

</details>

## Practical challenge

In `~/git-practice/assess-10-practical`:

1. Create an Ed25519 key pair `~/.ssh/assess_key` (no passphrase for this exercise) with the comment
   `ada@example.com`.
2. Add `https://github.com/octocat/Hello-World.git` as `origin` and verify you can read it.
3. Switch `origin` to the SSH form.
4. Configure **this repository only** to rewrite any `https://github.com/` URL to SSH with `url.<base>.insteadOf`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=ED25519; contains=refs/heads/master; output -->
```bash
cd ~/git-practice/assess-10-practical
ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/assess_key -N ""
ssh-keygen -l -f ~/.ssh/assess_key.pub | awk '{print $1, $3, $4}'
git remote add origin https://github.com/octocat/Hello-World.git
git ls-remote --heads origin | grep master
git remote set-url origin git@github.com:octocat/Hello-World.git
git config url."git@github.com:".insteadOf "https://github.com/"
git remote -v
```

```text
256 ada@example.com (ED25519)
7fd1a60b01f91b314f59955a4e4d4e80d8edf11d	refs/heads/master
origin	git@github.com:octocat/Hello-World.git (fetch)
origin	git@github.com:octocat/Hello-World.git (push)
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-10-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "Ed25519 key pair"                 'ssh-keygen -l -f ~/.ssh/assess_key.pub | grep -q ED25519 && [ -f ~/.ssh/assess_key ]'
check "key comment is ada@example.com"   'grep -q "ada@example.com" ~/.ssh/assess_key.pub'
check "origin uses SSH"                  'git remote get-url origin | grep -q "^git@github.com:octocat/Hello-World.git$"'
check "insteadOf set in this repository" 'git config --local --get url.git@github.com:.insteadOf | grep -q "https://github.com/"'
check "not set globally"                 '! git config --global --get url.git@github.com:.insteadOf'
```

```text
ok       Ed25519 key pair
ok       key comment is ada@example.com
ok       origin uses SSH
ok       insteadOf set in this repository
ok       not set globally
```

## Troubleshooting challenge

In `~/git-practice/assess-10-broken`, a teammate set up the remote from memory:

<!-- test: contains=Hello-Wrld; output -->
```bash
cd ~/git-practice/assess-10-broken
git remote add origin https://github.com/octocat/Hello-Wrld.git
git remote -v
```

```text
origin	https://github.com/octocat/Hello-Wrld.git (fetch)
origin	https://github.com/octocat/Hello-Wrld.git (push)
```

Symptom (in this course prompts are disabled; on your computer you would see a username prompt):

<!-- test: fail; contains=could not read Username; output -->
```bash
git ls-remote origin 2>&1
```

```text
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

Make `origin` readable without typing any credentials.

<details>
<summary>Solution</summary>

The repository is public, so a credential request means GitHub does not know this name (it does not reveal whether a
private repository exists). The name has a typo: fix the URL instead of entering credentials.

<!-- test: contains=refs/heads/master; output -->
```bash
git remote set-url origin https://github.com/octocat/Hello-World.git
git ls-remote --heads origin
```

```text
7fd1a60b01f91b314f59955a4e4d4e80d8edf11d	refs/heads/master
b1b3f9723831141a31a1a7252a213e216ea76e56	refs/heads/octocat-patch-1
b3cbd5bbd7e81436d2eee04537ea2b4c0cad4cdf	refs/heads/test
```

</details>

Verification:

<!-- test: contains=Hello-World.git; output -->
```bash
git remote get-url origin
git ls-remote --exit-code origin HEAD > /dev/null && echo "origin is reachable"
```

```text
https://github.com/octocat/Hello-World.git
origin is reachable
```

## Real-world scenario

A new colleague's CI job fails with `fatal: could not read Username for 'https://github.com'` while cloning a private
Helm chart repository. Their laptop works fine. What do you check?

<details>
<summary>Model answer</summary>

The laptop has a credential helper with the colleague's token; the CI runner has none. Check the URL first (typos
look the same), then give the job its own least-privilege credential: in GitHub Actions the `GITHUB_TOKEN` (with
access to that repository) or a fine-grained token / deploy key stored as a CI secret, never a personal password
(lessons 44, 48–50). Do not paste personal tokens into the pipeline definition.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-10-practical ~/git-practice/assess-10-broken ~/.ssh/assess_key ~/.ssh/assess_key.pub
```
