<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 01 · What is Git? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without opening the file, print the content of `prices.txt` as it was in the **first** commit, and show which lines
were added between the first and the latest commit.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-01/with-git
first=$(git rev-list --max-parents=0 HEAD)
git show "$first":prices.txt
git diff "$first" HEAD
```

```text
espresso 2.50
latte 3.20
diff --git a/prices.txt b/prices.txt
index df45f17..051d8e7 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,2 +1,4 @@
 espresso 2.50
-latte 3.20
+latte 3.30
+cappuccino 3.40
+mocha 3.90
```

`git rev-list --max-parents=0 HEAD` finds the root commit (the one with no parent). Lessons 13–15 cover history and
diffs in depth.

</details>
