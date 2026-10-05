<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 27 · Resolving merge conflicts · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Configure Git to refuse commits that contain conflict markers, using a hook that runs `git diff --cached --check`
(hooks are lesson 82; this is a preview).

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-27
printf '#!/bin/sh\nexec git diff --cached --check\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
printf '<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> other\n' > test.txt && git add test.txt
git commit -m "Test" 2>&1
```

```text
test.txt:1: leftover conflict marker
test.txt:3: leftover conflict marker
test.txt:5: leftover conflict marker
```

</details>
