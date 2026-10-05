<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 63 · Interactive rebase · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Use `--fixup` and `--autosquash`: change the espresso price, commit it as a fixup of "Add prices", and fold it in.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-63
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt
git commit -q -a --fixup=4267004
git log --oneline -1
GIT_SEQUENCE_EDITOR=true git rebase -q -i --autosquash fc345e6
git log --oneline
git show ':/^Add prices' | grep "^+espresso"
```

```text
2cc5415 (HEAD -> main) fixup! Add prices
0006fb5 (HEAD -> main) Add chai with its price
cb5bae3 Add green tea
825cce0 Add prices
fc345e6 Add the menu
d6df412 Add README
+espresso 2.60
```

`--fixup` creates a commit named `fixup! Add prices`; `--autosquash` moves it right below "Add prices" and turns it
into `fixup`. The rebase must start **before** "Add prices" (at `fc345e6`, "Add the menu"), so it is included; the
later commits get new IDs because their parent changed.

</details>
