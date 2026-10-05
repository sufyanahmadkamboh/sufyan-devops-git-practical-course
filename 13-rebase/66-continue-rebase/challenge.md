<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 66 · Continuing a rebase · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Mid-rebase, change your mind about the remaining steps: start an interactive rebase with `edit` on the first commit,
then use `--edit-todo` to drop "Price mocha" before continuing.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-66
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~3
GIT_EDITOR="sed -i '/Price mocha/s/^pick/drop/'" git rebase --edit-todo
git rebase --continue > /dev/null
git log --oneline -3
```

```text
Stopped at 33f0085...  # Price green tea
You can amend the commit now, with

  git commit --amend 

Once you are satisfied with your changes, run

  git rebase --continue
e49b0d2 (HEAD -> main) Add mocha
33f0085 Price green tea
49037db Add tea notes
```

</details>
