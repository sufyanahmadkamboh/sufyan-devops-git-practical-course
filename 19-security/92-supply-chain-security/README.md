# Lesson 92 · Supply chain security

> Level 19 · Git security · ⏱ 25 minutes

## What are we learning?

Your software is built from repositories you do not control: libraries, Helm charts, GitHub Actions, base images.
The Git-level risks: **mutable references** (a tag or branch can be moved to malicious code), **spoofed authors**,
**compromised accounts** and **malicious commits** hidden in large changes. We exploit a moved tag locally, then pin by
commit ID.

## Visual

```text
 your workflow:  uses: some-org/deploy-action@v2          ← a tag: the owner (or an attacker with their token)
                                                              can move it to any commit, any time
                 uses: some-org/deploy-action@3f9a1c…     ← a full commit ID: immutable content

 trust signals:  signed commits/tags from known keys · protected branches with reviews · trusted publishers ·
                 Dependabot/Renovate updating pins through PRs · least-privilege tokens in CI
```

## Lab setup

A "library" repository published by someone else, and your project that uses its `v1.0.0`:

<!-- test: contains=lesson-92 -->
```bash
bash scripts/new-lab.sh lesson-92 empty
cd ~/git-practice/lesson-92
git init -q --bare lib.git
git clone -q lib.git lib-author 2> /dev/null && cd lib-author
printf '#!/bin/sh\necho "deploying the cafe"\n' > deploy.sh && git add deploy.sh && git commit -q -m "Add deploy script"
git tag -a v1.0.0 -m "Release 1.0.0" && git push -q origin HEAD:main v1.0.0
cd .. && git clone -q --branch v1.0.0 lib.git consumer 2> /dev/null && sh consumer/deploy.sh
```

## Demonstration

Pinning by **tag** trusts that the tag never moves. An attacker who gained push access moves it:

<!-- test: contains=forced update; output -->
```bash
cd lib-author
printf '#!/bin/sh\necho "deploying the cafe"\necho "(also sending your credentials somewhere)"\n' > deploy.sh
git commit -q -am "Improve logging"
git tag -f -a v1.0.0 -m "Release 1.0.0" > /dev/null
git push -f origin v1.0.0 2>&1 | grep -E "forced|v1.0.0"
```

```text
 + bc48973...9c52797 v1.0.0 -> v1.0.0 (forced update)
```

The next build that fetches `v1.0.0` runs different code under the same name:

<!-- test: contains=sending your credentials; output -->
```bash
cd .. && rm -rf consumer && git clone -q --branch v1.0.0 lib.git consumer 2> /dev/null
sh consumer/deploy.sh
```

```text
deploying the cafe
(also sending your credentials somewhere)
```

## Command breakdown

| Practice | Commands / settings |
|---|---|
| pin dependencies to commit IDs | `uses: org/action@<40-char sha>`, `git rev-parse v1.0.0^{commit}` |
| resolve a tag before pinning | `git ls-remote https://github.com/actions/checkout refs/tags/v4` |
| verify signed tags/commits | `git verify-tag`, `git log --format='%G? %h %an'` |
| detect moved tags | compare stored IDs; Git refuses to overwrite existing local tags on fetch |
| least privilege in CI | `permissions: contents: read` in workflows, fine-grained tokens |
| updates through review | Dependabot / Renovate PRs that bump the pinned SHA |

## Hands-on exercise

**Instructions.** Pin the consumer to the **commit ID** the original `v1.0.0` pointed to (the "Add deploy script"
commit), and run it.

**Expected result.** Only "deploying the cafe".

<!-- test-run: cd ~/git-practice/lesson-92 && rm -rf pinned && git clone -q lib.git pinned 2> /dev/null && git -C pinned switch -q --detach "$(git -C lib-author log --format=%H --grep='Add deploy script')" -->

**Verification.**

<!-- test: absent=credentials; contains=deploying the cafe -->
```bash
cd ~/git-practice/lesson-92
sh pinned/deploy.sh
git -C pinned log --oneline -1
```

## Break it

Authorship is not identity. Ada makes a commit claiming to be Grace, the maintainer everybody trusts:

<!-- test: contains=Grace Hopper; output -->
```bash
cd ~/git-practice/lesson-92/lib-author
echo "# reviewed by Grace" >> deploy.sh
git -c user.name="Grace Hopper" -c user.email="grace@example.com" commit -q -am "Security fix"
git log -1 --format='%h %an <%ae> %s'
```

```text
bc42bcd Grace Hopper <grace@example.com> Security fix
```

## Troubleshoot

`git log` happily shows "Grace Hopper": author fields are free text. On GitHub, the commit would even show Grace's
avatar if her email is public. The only Git-level evidence is the **signature**, and this commit has none:

<!-- test: contains=N Grace Hopper; output -->
```bash
git log -1 --format='%G? %an %s'
```

```text
N Grace Hopper Security fix
```

`N` = no signature (`G` would be a good signature from a trusted key, lesson 91).

## Fix

Make unsigned or unverified commits stand out, and refuse them where it matters:

<!-- test: contains=unsigned; output -->
```bash
git log --format='%G? %h %an %s' | awk '$1 != "G" {print "unsigned: " $0}'
```

```text
unsigned: N bc42bcd Grace Hopper Security fix
unsigned: N 032597a Ada Lovelace Improve logging
unsigned: N 94faffe Ada Lovelace Add deploy script
```

On GitHub: branch protection "Require signed commits", "vigilant mode" (shows **Unverified** on commits that claim to
be you but are not signed by you), required reviews from CODEOWNERS, and 2FA (with passkeys or hardware keys) for every
account, so a stolen password alone cannot push.

## Real-world example

Real incidents followed exactly these patterns: popular GitHub Actions whose version tags were repointed to code that
dumped CI secrets into logs (pipelines using `@v1` tags were affected; pipelines pinned to SHAs were not), compromised
maintainer accounts publishing malicious releases, and backdoors hidden in large "maintenance" commits by contributors
who had built trust over years. Defences are layered: pin, verify, review, least privilege, and monitor.

## Practice challenge

Resolve the current commit ID behind a public tag, as you would before pinning an action.

<details>
<summary>Solution</summary>

<!-- test: contains=refs/tags/v4; output -->
```bash
git ls-remote https://github.com/actions/checkout refs/tags/v4 'refs/tags/v4^{}'
```

```text
11d5960a326750d5838078e36cf38b85af677262	refs/tags/v4
```

For an annotated tag, the `^{}` line is the commit it points to: pin that 40-character ID, with the tag name as a
comment (`uses: actions/checkout@<sha> # v4`).

</details>

## Recap

- Tags and branches are mutable; commit IDs are not: pin dependencies by commit ID.
- Author names are claims; trust signatures from known keys, reviews and protected branches.
- Least-privilege tokens and 2FA limit what a compromised account or action can do.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-92
```

Next: [Module 20 · Lesson 93 · GitHub Issues](../../20-github-advanced/93-github-issues/README.md).
