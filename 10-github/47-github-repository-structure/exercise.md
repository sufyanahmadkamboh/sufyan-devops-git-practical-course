<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 47 · GitHub repository structure · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Print the URL of every tab of your practice repository.

**Expected result.** Seven URLs ending in `/issues`, `/pulls`, `/actions`, ...

**Verification.**

```bash
url=$(gh repo view --json url --jq .url)
for tab in "" /issues /pulls /actions /releases /branches /tags; do echo "$url$tab"; done
```
