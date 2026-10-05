<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 10 · The staging area · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Put two changes **in the same file** into two different commits: add `chai` at the end of `menu.txt` and change
`espresso` to `ristretto` at the top, then commit them separately. (Hint: `git add -p`, answering `y`/`n` per hunk.)

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-10
printf 'ristretto\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git diff
# git add -p asks about each hunk. Both edits are close together, so Git shows them as ONE hunk:
# "s" splits it, then "y" stages the first part and "n" skips the second.
printf 's\ny\nn\n' | git add -p menu.txt > /dev/null
git commit -q -m "Rename espresso to ristretto"
git add menu.txt && git commit -q -m "Add mocha"
git log --oneline -2
```

```text
diff --git a/menu.txt b/menu.txt
index 02e91d0..52d5b90 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,5 +1,6 @@
-espresso
+ristretto
 latte
 cappuccino
 green tea
 chai
+mocha
97cd3f4 (HEAD -> main) Add mocha
8d52e67 Rename espresso to ristretto
```

`git add -p` splits a file's changes into hunks and asks for each one (`y` yes, `n` no, `s` split, `q` quit, `?`
help); that is how one file's changes end up in two commits.

</details>
