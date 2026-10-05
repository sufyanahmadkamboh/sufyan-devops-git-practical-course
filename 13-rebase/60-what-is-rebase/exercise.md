<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 60 · What is rebase? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Prove that the rebased commit contains the same **change** as the original (compare the patches),
even though the IDs differ.

**Expected result.** The two patch IDs are equal. (`feature-tea@{1}` is the branch's previous position in its reflog:
the commit before the rebase.)

**Verification.**

```bash
cd ~/git-practice/lesson-60
git show 'feature-tea@{1}' | git patch-id | cut -c1-12
git show feature-tea | git patch-id | cut -c1-12
```

```text
a8a3c0bf8d69
a8a3c0bf8d69
```
