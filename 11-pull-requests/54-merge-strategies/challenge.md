<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 54 · Merge strategies · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Merge a real PR on your practice repository with **squash**, deleting its branch, and show the resulting commit on
GitHub's `main`.

<details>
<summary>Solution</summary>

<!-- test-run github: gh auth setup-git -->

```bash
cd ~/git-practice/lesson-54-gh
git push -q origin --delete chai 2> /dev/null || true
git switch -q -c chai
echo "chai" >> menu.txt && git commit -q -am "Add chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git push -q -u origin chai 2> /dev/null
gh pr create --base main --title "Add chai" --body "Chai on the menu, with its price." > /dev/null
gh pr merge chai --squash --delete-branch > /dev/null 2>&1
git switch -q main && git pull -q
git log --oneline -1
```

```text
0703734 (HEAD -> main, origin/main, origin/HEAD) Add chai (#11)
```

GitHub's squash commit subject is the PR title with the PR number: `Add chai (#N)`.

</details>
