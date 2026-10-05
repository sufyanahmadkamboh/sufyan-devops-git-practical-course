<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 67 · Cherry-pick · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Cherry-pick the fix again onto a new branch `release-1.0` from `4267004`, recording where it came from.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-67
git switch -q -c release-1.0 4267004
git cherry-pick -x "$(git log --format=%h --grep='Fix the cappuccino' feature-specials)" > /dev/null
git log -1 --format=%B
```

```text
Fix the cappuccino price (charged too little)

(cherry picked from commit 702fad1e348bc4b10b305335569269d691d57816)
```

</details>
