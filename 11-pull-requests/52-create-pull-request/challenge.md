<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 52 · Creating a pull request · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Open a **draft** PR from a new branch, then mark it ready for review, and close it (with its branch) to keep the
practice repository tidy.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-52
git switch -q main && git switch -q -c try-draft
echo "draft idea" > idea.txt && git add idea.txt && git commit -q -m "Draft idea"
git push -q -u origin try-draft 2> /dev/null
gh pr create --draft --base main --title "Draft idea" --body "Work in progress" > /dev/null
gh pr ready try-draft > /dev/null
gh pr view try-draft --json isDraft --jq .isDraft
gh pr close try-draft --delete-branch > /dev/null 2>&1
```

```text
✓ Pull request sufyanahmadkamboh/git-practice-cafe#9 is marked as "ready for review"
false
```

</details>
