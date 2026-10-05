<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 77 · Branches are references · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Fetch-style: create a reference outside `refs/heads` (`refs/review/42`) pointing at `feature-tea`, and list it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-77
git update-ref refs/review/42 feature-tea
git for-each-ref refs/review
git branch | grep -c review || true
```

```text
bb676741936c50ad1f936300a05fc3c2cc0a9675 commit	refs/review/42
0
```

It is a valid reference (usable in any command: `git log refs/review/42`), but not a branch, so `git branch` does not
list it.

</details>
