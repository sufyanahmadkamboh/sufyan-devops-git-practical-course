<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 42 · git push · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace pushes first; then Ada:

```bash
cd ../grace && git pull -q && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git push 2>&1
```

```text
To ~/git-practice/lesson-42/server/cafe.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '~/git-practice/lesson-42/server/cafe.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

`! [rejected] main -> main (fetch first)`: the server's `main` has a commit (Grace's) that Ada does not have. A push
must be a fast-forward of the server's branch; accepting Ada's push would delete Grace's commit from `main`.
(`non-fast-forward` is the same rejection when Git already knows the remote commit from an earlier fetch.)

## Fix

Integrate first, then push. **Not** `--force`.

```bash
git pull -q --rebase
git push
git log --oneline -3
```

```text
To ~/git-practice/lesson-42/server/cafe.git
   c234723..3f3ebb8  main -> main
3f3ebb8 (HEAD -> main, origin/main, origin/HEAD) Espresso 2.60
c234723 Add mocha
d4540f4 Add green tea
```

Both commits are on the server: Grace's, then Ada's on top.
