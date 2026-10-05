<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 24 · Fast-forward merge · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Undo the last fast-forward merge on `main` (the label should move back to where it was before) without losing the
branch's commit.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-24
git reset -q --hard ORIG_HEAD
git log --oneline --graph -3 main feature-mocha
```

```text
* 8109406 (feature-mocha) Price mocha
* 45d6d00 (HEAD -> main, feature-chai) Add chai
*   d986fad Merge branch 'feature-hours'
|\  
```

A merge records the previous position of the branch in `ORIG_HEAD`. Moving `main` back is safe here because nothing was
pushed; the commits still exist on `feature-mocha` (lesson 31 explains `reset`).

</details>
