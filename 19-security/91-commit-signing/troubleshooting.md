<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 91 · Commit signing · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A teammate clones the repository and verifies Ada's latest commit:

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
