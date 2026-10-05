# Lesson 91 · Commit signing

> Level 19 · Git security · ⏱ 30 minutes

## What are we learning?

Anyone can write any name and email into a commit (lesson 04: it is just configuration). A **signature** proves that
the commit was made by the holder of a private key. We sign commits and tags with an SSH key (simplest, Git 2.34+),
verify them, and see how GPG does the same.

## Visual

```text
 git commit -S        commit object + signature made with YOUR private key
                                 │
 git verify-commit    checks the signature with the PUBLIC key:
                        SSH:  allowed_signers file  ("ada@example.com ssh-ed25519 AAAA…")
                        GPG:  your keyring
                      GitHub: the public key uploaded as a "signing key" → "Verified" badge

 author name/email = a claim · valid signature from a trusted key = proof
```

## Lab setup

A signing key (an SSH key can sign; in real life use your existing key, with a passphrase):

<!-- test: contains=lesson-91 -->
```bash
bash scripts/new-lab.sh lesson-91 basic
cd ~/git-practice/lesson-91
mkdir -p ~/.ssh && chmod 700 ~/.ssh
[ -f ~/.ssh/id_signing ] || ssh-keygen -q -t ed25519 -C "ada@example.com" -f ~/.ssh/id_signing -N ""
ls ~/.ssh | grep signing
```

## Demonstration

Configure Git to sign with that SSH key:

<!-- test: contains=ssh -->
```bash
git config gpg.format ssh
git config user.signingkey "$HOME/.ssh/id_signing.pub"
git config --get gpg.format
```

Sign a commit with `-S`:

<!-- test: contains=Add green tea -->
```bash
echo "green tea" >> menu.txt && git commit -q -S -am "Add green tea"
git log --oneline -1
git cat-file -p HEAD | sed -n '/gpgsig/,/END SSH SIGNATURE/p' | head -3
```

The signature is part of the commit object. To **verify**, Git needs to know which keys to trust for which email: the
allowed signers file.

<!-- test: contains=Good "git" signature for ada@example.com; output -->
```bash
echo "ada@example.com $(cat ~/.ssh/id_signing.pub)" > ~/.ssh/allowed_signers
git config gpg.ssh.allowedSignersFile "$HOME/.ssh/allowed_signers"
git verify-commit HEAD 2>&1 | sed "s|$HOME|~|"
```

```text
Good "git" signature for ada@example.com with ED25519 key SHA256:26wG0fLnNNF6vVyYVwEA66m+t7NSNSijllSiFb0Wmic
```

## Command breakdown

| Command / setting | Use |
|---|---|
| `git config gpg.format ssh` | sign with SSH keys (default: `openpgp` = GPG) |
| `git config user.signingkey KEY` | the key (SSH: the `.pub` path; GPG: the key ID) |
| `git config commit.gpgsign true` / `tag.gpgsign true` | sign every commit / tag automatically |
| `git commit -S`, `git tag -s` | sign one commit / tag |
| `git verify-commit C`, `git verify-tag T` | verify |
| `git log --show-signature` / `--format='%G? %h %s'` | signatures in the log (`G` good, `N` none, `B` bad, `U` unknown key) |

## Hands-on exercise

**Instructions.** Sign every commit automatically, make one more commit, and list the signature status of the last
three commits.

**Expected result.** `G` for the two signed commits, `N` for the unsigned "Add prices".

<!-- test-run: cd ~/git-practice/lesson-91 && git config commit.gpgsign true && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" -->

**Verification.**

<!-- test: contains=G ; contains=N  -->
```bash
cd ~/git-practice/lesson-91
git log --format='%G? %h %s' -3
```

## Break it

A teammate clones the repository and verifies Ada's latest commit:

<!-- test: fail; contains=allowedSignersFile needs to be configured; output -->
```bash
git clone -q . ../lesson-91-teammate
git -C ../lesson-91-teammate verify-commit HEAD 2>&1
```

```text
error: gpg.ssh.allowedSignersFile needs to be configured and exist for ssh signature verification
```

## Troubleshoot

`gpg.ssh.allowedSignersFile needs to be configured and exist for ssh signature verification`: a signature alone proves
nothing until you decide whose public key you trust for which identity. For SSH signing that decision is the
allowed signers file; for GPG it is your keyring and its trust settings; on GitHub it is the keys users upload.

## Fix

Teams commit an allowed signers file to the repository (reviewed like code), and each clone points Git at it:

<!-- test: contains=Good "git" signature; output -->
```bash
mkdir -p .github && cp ~/.ssh/allowed_signers .github/allowed_signers
git add .github/allowed_signers && git commit -q -m "Add the team's allowed signers"
cd ../lesson-91-teammate && git pull -q
git config gpg.ssh.allowedSignersFile .github/allowed_signers
git verify-commit HEAD 2>&1 | sed "s|$HOME|~|"
```

```text
Good "git" signature for ada@example.com with ED25519 key SHA256:26wG0fLnNNF6vVyYVwEA66m+t7NSNSijllSiFb0Wmic
```

## Real-world example

On GitHub, upload the same public key under Settings → SSH and GPG keys → **New SSH key → Key type: Signing key**;
commits signed with it show **Verified**. Branch protection can then "Require signed commits", and release tags are
signed (`git tag -s v1.2.0`) so that consumers can check who released them. With GPG, the steps are the same with
`gpg --full-generate-key`, `git config user.signingkey <KEYID>`, and the GPG public key uploaded instead.

## Practice challenge

Create a **signed annotated tag** for the release and verify it.

<details>
<summary>Solution</summary>

<!-- test: contains=Good "git" signature for ada@example.com; output -->
```bash
cd ~/git-practice/lesson-91
git tag -s v1.0.0 -m "Release 1.0.0"
git verify-tag v1.0.0 2>&1 | sed "s|$HOME|~|"
```

```text
Good "git" signature for ada@example.com with ED25519 key SHA256:26wG0fLnNNF6vVyYVwEA66m+t7NSNSijllSiFb0Wmic
```

</details>

## Recap

- Author fields are claims; signatures are proof of key possession.
- SSH signing: `gpg.format ssh`, `user.signingkey`, `commit.gpgsign`; verify with an allowed signers file.
- Upload the signing key to GitHub for "Verified", and require signed commits on protected branches.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-91 ~/git-practice/lesson-91-teammate
```

Next: [Lesson 92 · Supply chain security](../92-supply-chain-security/README.md).
