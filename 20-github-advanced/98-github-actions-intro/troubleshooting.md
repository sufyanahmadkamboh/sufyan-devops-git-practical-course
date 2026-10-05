<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 98 · GitHub Actions introduction · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A careless edit pushed to `main`: a price without decimals.

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

```text
failure
```

## Troubleshoot

The commit shows a red ✗ on GitHub. The failed step's log says exactly what is wrong:

```bash
run=$(gh run list --workflow check-prices --limit 10 --json databaseId,displayTitle \
  --jq '[.[] | select(.displayTitle == "Add flat white")][0].databaseId')
gh run view "$run" --log-failed | sed -n '/invalid lines:$/,/exit code/p' | sed -E 's/^.*Z //'
```

```text
invalid lines:
flat white,3
##[error]Process completed with exit code 1.
```

## Fix

Fix the data in a new commit; the next run goes green:

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

```text
success
```

With branch protection requiring `check-prices` (lesson 59), the broken commit could not have reached `main` at all:
it would have been a red PR instead.
