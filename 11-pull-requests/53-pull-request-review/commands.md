<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 53 · Pull request review · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-53 github
cd ~/git-practice/lesson-53
```

```bash
git switch -q -c price-green-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git push -q -u origin price-green-tea 2> /dev/null
gh pr create --base main --title "Price green tea" --body "Adds the green tea price."
```

## Demonstration

```bash
gh pr review price-green-tea --comment --body "Looks good overall. One question on the price, see the line comment."
gh pr view price-green-tea --json reviews --jq '.reviews[] | "\(.state): \(.body)"'
```

```bash
me=$(gh api user --jq .login)
number=$(gh pr view price-green-tea --json number --jq .number)
commit=$(git rev-parse HEAD)
body=$(printf 'Our prices include tax: 2.80 is the price before tax.\n```suggestion\ngreen tea 2.90\n```')
gh api "repos/$me/git-practice-cafe/pulls/$number/comments" \
  -f body="$body" -f commit_id="$commit" -f path=prices.txt -F line=4 -f side=RIGHT --jq '"\(.path):\(.line) \(.body)"'
```

```bash
sed -i 's/^green tea 2.80$/green tea 2.90/' prices.txt
git commit -q -am "Price green tea with tax" && git push -q 2> /dev/null
```

```bash
gh pr diff price-green-tea
```

## Hands-on exercise

```bash
me=$(gh api user --jq .login)
number=$(gh pr view price-green-tea --json number --jq .number)
gh api "repos/$me/git-practice-cafe/pulls/$number/comments" --jq '.[] | "\(.path):\(.original_line) \(.user.login)"'
```

## Break it

```bash
gh pr review price-green-tea --approve 2>&1
```

## Fix

```bash
gh pr review price-green-tea --approve --body "Price with tax confirmed. Thanks!"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-53
gh pr comment price-green-tea --body "Reviewed following docs/review-guidelines.md" > /dev/null
gh pr view price-green-tea --json comments,reviews --jq '"comments: \(.comments | length), reviews: \(.reviews | length)"'
```

## Cleanup

```bash
cd ~/git-practice/lesson-53
gh pr close price-green-tea --delete-branch > /dev/null 2>&1
```

```bash
cd ~ && rm -rf ~/git-practice/lesson-53
```
