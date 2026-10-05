<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 94 · Labels · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Close the espresso issue as completed and remove the team labels created here (keep the defaults).

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-94
for n in $(gh issue list --state open --json number,title --jq '.[] | select(.title | startswith("Espresso is charged")) | .number'); do
  gh issue close "$n" --reason completed > /dev/null
done
gh label delete "priority:high" --yes && gh label delete "area:prices" --yes
gh label list --json name --jq '.[].name' | grep -c ":" || true
```

```text
✓ Closed issue sufyanahmadkamboh/git-practice-cafe#41 (Espresso is charged 2.40 instead of 2.50)
0
```

</details>
