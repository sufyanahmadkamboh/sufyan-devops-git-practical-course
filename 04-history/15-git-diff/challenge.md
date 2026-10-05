<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 15 · git diff · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without committing, prove whether your working directory differs from the `feature-tea` branch in `README.md`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-15
git diff feature-tea -- README.md
```

```text
diff --git a/README.md b/README.md
index af07f28..742be8c 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,5 @@
 # Cafe
 
 The menu and prices of a small cafe.
+
+Open every day from 8:00 to 18:00.
```

`git diff <commit>` compares that commit with your working directory. `main` has the opening hours, `feature-tea`
does not, so the README differs.

</details>
