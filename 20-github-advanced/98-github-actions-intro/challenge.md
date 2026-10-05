<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 98 · GitHub Actions introduction · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Add `workflow_dispatch` so the check can be started by hand, start it, and list the run.

<details>
<summary>Solution</summary>

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

```text
workflow_dispatch queued
```

</details>
