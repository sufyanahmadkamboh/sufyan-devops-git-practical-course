<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 33 · git reflog · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

List the last positions of `main` with their times instead of `@{N}` numbers.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-33
git reflog show --date=relative main | head -3 | sed -E 's/[0-9]+ (seconds?|minutes?) ago/N seconds ago/'
```

```text
ecff18a (HEAD -> main, rescue) main@{N seconds ago}: reset: moving to HEAD@{1}
6833580 main@{N seconds ago}: reset: moving to HEAD~3
ecff18a (HEAD -> main, rescue) main@{9 months ago}: commit: Price mocha
```

`--date=relative` replaces `@{N}` with times (the `sed` only keeps the output stable here). `git show main@{10.minutes.ago}`
uses such times directly.

</details>
