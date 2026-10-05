<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 70 · Git bisect · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Let Git do the whole search with `git bisect run`.

**Expected result.** The first bad commit is "Add mocha".

**Verification.**

```bash
cd ~/git-practice/lesson-70
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh > /dev/null 2>&1
git log -1 --format='first bad commit: %h %s' refs/bisect/bad
git bisect reset > /dev/null 2>&1
```
