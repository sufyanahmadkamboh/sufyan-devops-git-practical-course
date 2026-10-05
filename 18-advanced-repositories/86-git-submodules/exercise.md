<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 86 · Git submodules · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** The shared repository gets a new rule. Update the cafe's submodule to it and commit the new pin.

**Expected result.** `git diff` of the main repository shows the submodule moving to a new commit; after committing,
`shared/` contains the new rule.

**Verification.**

```bash
cd ~/git-practice/lesson-86
git -c protocol.file.allow=always submodule update -q --remote shared
git diff --submodule=log | head -3
git commit -q -am "Update the shared rules"
cat shared/tax.txt
```
