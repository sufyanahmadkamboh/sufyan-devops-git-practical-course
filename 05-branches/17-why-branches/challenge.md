<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 17 · Why branches exist · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Start two features at the same time from `main` in `lesson-17b` (`feature-a` and `feature-b`, one commit each) and
show that neither contains the other's commit.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-17b
git switch -q -c feature-a main && echo a > a.txt && git add a.txt && git commit -q -m "Feature A"
git switch -q -c feature-b main && echo b > b.txt && git add b.txt && git commit -q -m "Feature B"
git log --oneline --graph feature-a feature-b main
```

```text
* 5ae7060 (feature-a) Feature A
| * 6d0e1b3 (HEAD -> feature-b) Feature B
|/  
* 18c8f11 (main) Fix the latte price
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Both branch off `main`; each has its own commit; neither sees the other.

</details>
