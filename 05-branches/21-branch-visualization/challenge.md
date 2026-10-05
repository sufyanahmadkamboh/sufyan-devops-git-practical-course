<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 21 · Branch visualization · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Make the graph show **three** tips: `main`, `feature` and a new `experiment` branch that forks from `feature`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-21
git switch -q -c experiment feature
echo "oat milk" >> menu.txt && git commit -q -am "Try oat milk"
git log --oneline --graph --all
```

```text
* e5e6b92 (HEAD -> experiment) Try oat milk
* c8c4b19 (feature) Add chai
* de65bec Add green tea
| * 9f920d9 (main) Add hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

</details>
