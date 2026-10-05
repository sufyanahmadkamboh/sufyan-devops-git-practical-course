<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 48 · HTTPS authentication · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** After the fix below, show which credential helper Git uses for github.com and in which file it is
configured.

**Expected result.** gh's `auth git-credential` command (or `manager` if you use Git Credential Manager), in `~/.gitconfig`.

<!-- test-run github: gh auth setup-git -->

**Verification.**

```bash
git config --show-origin --get-all credential.https://github.com.helper
```

<!-- test-run github: git config --global --unset-all credential.https://github.com.helper || true -->
