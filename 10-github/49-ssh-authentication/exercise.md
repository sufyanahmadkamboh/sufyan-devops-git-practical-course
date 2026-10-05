<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 49 · SSH authentication · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Print your public key, the text you would paste into GitHub's "New SSH key" form.

**Expected result.** One line starting with `ssh-ed25519` and ending with your comment.

**Verification.**

```bash
cat ~/.ssh/id_ed25519.pub
```
