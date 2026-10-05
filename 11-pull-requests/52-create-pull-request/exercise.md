<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 52 · Creating a pull request · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Push a second commit (the price) to the branch, and check that the PR now has two commits.

**Expected result.** `2 commit(s)`.

<!-- test-run github: cd ~/git-practice/lesson-52 && echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea" && git push -q 2> /dev/null -->

**Verification.**

```bash
cd ~/git-practice/lesson-52
gh pr view add-green-tea --json commits --jq '"\(.commits | length) commit(s)"'
```
