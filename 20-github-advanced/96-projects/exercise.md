<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 96 · Projects · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** In the web interface, create a board project "Cafe roadmap", link it to `git-practice-cafe`, add the
open issues from lesson 95, and set one to **In progress**.

**Expected result.** The repository's **Projects** tab lists "Cafe roadmap".

**Verification** (needs the `project` scope):

```bash
me=$(gh api user --jq .login)
gh project list --owner "$me" --format json --jq '.projects[].title'
```
