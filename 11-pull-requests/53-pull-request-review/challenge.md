<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 53 · Pull request review · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Add a conversation comment (not a review) linking to the review guidelines, then count all comments on the PR.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-53
gh pr comment price-green-tea --body "Reviewed following docs/review-guidelines.md" > /dev/null
gh pr view price-green-tea --json comments,reviews --jq '"comments: \(.comments | length), reviews: \(.reviews | length)"'
```

```text
comments: 1, reviews: 2
```

</details>
