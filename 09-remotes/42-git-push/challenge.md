<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 42 · git push · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show that `--force-with-lease` protects Grace's work: Ada rewrites her last commit and force-pushes with lease after
Grace pushed something new that Ada has not fetched.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-42/grace && git pull -q && echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../ada && git commit -q --amend -m "Raise the espresso price to 2.60"
git push --force-with-lease 2>&1 || true
```

```text
To ~/git-practice/lesson-42/server/cafe.git
 ! [rejected]        main -> main (stale info)
error: failed to push some refs to '~/git-practice/lesson-42/server/cafe.git'
```

`(stale info)`: the server's `main` is not where Ada's `origin/main` says it was, so the push is refused. `--force`
would have succeeded and removed "Add chai".

</details>
