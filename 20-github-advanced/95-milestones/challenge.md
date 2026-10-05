<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 95 · Milestones · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Close all remaining issues of the milestone, then close the milestone itself.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-95
for n in $(gh issue list --milestone "v1.1.0" --state open --json number --jq '.[].number'); do gh issue close "$n" > /dev/null; done
me=$(gh api user --jq .login)
m=$(gh api "repos/$me/git-practice-cafe/milestones" --jq '.[] | select(.title=="v1.1.0") | .number')
gh api -X PATCH "repos/$me/git-practice-cafe/milestones/$m" -f state=closed --jq '"\(.title): \(.state)"'
```

```text
✓ Closed issue sufyanahmadkamboh/git-practice-cafe#39 (Update the menu board)
v1.1.0: closed
```

</details>
