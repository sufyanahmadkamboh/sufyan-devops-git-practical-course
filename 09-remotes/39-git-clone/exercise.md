<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 39 · git clone · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Make a shallow clone with only the latest commit of `feature-tea`.

**Expected result.** `git log` shows exactly one commit.

**Verification.**

```bash
cd ~/git-practice/lesson-39/shallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

Solution: `git clone --no-local --depth 1 --branch feature-tea server/cafe.git shallow`. For a local path, `--depth`
needs `--no-local` (or a `file://` URL); otherwise Git copies the files directly and ignores it. A GitHub URL needs
neither.
