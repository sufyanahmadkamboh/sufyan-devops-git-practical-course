<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 70 · Git bisect · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show the change that introduced the bug, and explain it.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-70
git show "$(git log --format=%h --grep='^Add mocha$')" -- prices.txt
```

```text
commit 3ceea031d6f34d67cc8f33c993ea0784c54ae95f
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:03:00 2026 +0000

    Add mocha

diff --git a/prices.txt b/prices.txt
index 88ea474..63b4ce4 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,5 @@
 espresso 2.50
 latte 3.20
 cappuccino 3.00
+mocha 3.90
+latte 3.60
```

The mocha commit also added a second `latte` line. `price.sh` greps `^latte `, gets two prices, and the sum breaks.

</details>
