<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 98 · GitHub Actions introduction · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-98 github
cd ~/git-practice/lesson-98
ls
```

## Demonstration

```bash
mkdir -p .github/workflows
cat > .github/workflows/check.yml << 'EOF'
name: check-prices
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Every line of prices.csv is "name,price"
        run: |
          bad=$(grep -vE '^[a-z -]+,[0-9]+\.[0-9]{2}$' prices.csv || true)
          if [ -n "$bad" ]; then echo "invalid lines:"; echo "$bad"; exit 1; fi
          echo "prices.csv OK ($(wc -l < prices.csv) items)"
EOF
git add .github/workflows/check.yml
git commit -q -m "ci: check the price file on every push" && git push -q 2> /dev/null
git log --oneline -1
```

```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "ci: check the price file on every push")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json status,conclusion,displayTitle --jq '"\(.displayTitle): \(.status), \(.conclusion)"'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-98
gh run list --workflow check-prices --limit 3 --json displayTitle,conclusion --jq '.[] | "\(.conclusion) \(.displayTitle)"'
```

## Break it

```bash
cd ~/git-practice/lesson-98
git pull -q
echo "flat white,3" >> prices.csv && git commit -q -am "Add flat white" && git push -q 2> /dev/null
git log --oneline -1
```

```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Add flat white")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json conclusion --jq .conclusion
```

## Troubleshoot

```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Add flat white")][0].databaseId')
gh run view "$run" --log-failed | sed -n '/invalid lines:$/,/exit code/p' | sed -E 's/^.*Z //'
```

## Fix

```bash
sed -i 's/^flat white,3$/flat white,3.00/' prices.csv
git commit -q -am "Fix the flat white price" && git push -q 2> /dev/null
git log --oneline -1
```

```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Fix the flat white price")][0].databaseId')
gh run watch "$run" --exit-status > /dev/null 2>&1 || true
gh run view "$run" --json conclusion --jq .conclusion
```

## Practice challenge

```bash
cd ~/git-practice/lesson-98
grep -q workflow_dispatch .github/workflows/check.yml || {
  sed -i 's/^  pull_request:$/  pull_request:\n  workflow_dispatch:/' .github/workflows/check.yml
  git commit -q -am "ci: allow manual runs" && git push -q 2> /dev/null
}
sleep 5
gh workflow run check-prices --ref main
```

```bash
gh run list --workflow check-prices --limit 1 --json event,status --jq '.[0] | "\(.event) \(.status)"'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-98
```
