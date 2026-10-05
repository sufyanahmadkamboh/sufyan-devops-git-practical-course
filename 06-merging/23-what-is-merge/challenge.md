<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 23 · What is a merge? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create two new branches from `main`, each adding a different new file, and merge both into `main`. How many merge
commits do you get?

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-23
git switch -q main
git switch -q -c a && echo a > a.txt && git add a.txt && git commit -q -m "Add a"
git switch -q main && git switch -q -c b && echo b > b.txt && git add b.txt && git commit -q -m "Add b"
git switch -q main
git merge -q --no-edit a
git merge -q --no-edit b
git log --oneline --graph -6
```

```text
*   febf353 (HEAD -> main) Merge branch 'b'
|\  
| * fe4994f (b) Add b
* | 5c7bb5e (a) Add a
|/  
*   8cb4ac7 (feature-tea) Merge branch 'feature-tea'
|\  
| * bb67674 Add green tea to the menu
* | f40d080 Add opening hours
|/  
```

The first merge is a fast-forward (no merge commit, `main` had not moved); the second needs a merge commit, because
`main` now has `Add a`, which `b` does not have.

</details>
