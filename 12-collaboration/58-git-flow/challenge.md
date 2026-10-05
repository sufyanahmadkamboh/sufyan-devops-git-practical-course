<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 58 · Git Flow · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Which commits would go into the next release (1.2.0) if it were cut now? Start a new feature first.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-58
git switch -q -c feature/mocha develop && echo mocha >> menu.txt && git commit -q -am "Add mocha"
git switch -q develop && git merge -q --no-ff --no-edit feature/mocha
git log --oneline --no-merges main..develop
```

```text
8718abb (feature/mocha) Add mocha
```

</details>
