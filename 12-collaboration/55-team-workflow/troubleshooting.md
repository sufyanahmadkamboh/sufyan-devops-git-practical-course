<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 55 · Team Git workflow · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Two developers commit directly on `main` and push, minutes apart:

```bash
cd ~/git-practice/lesson-55/grace && git pull -q
echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../linus && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

```text
To ~/git-practice/lesson-55/server/cafe.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '~/git-practice/lesson-55/server/cafe.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

Linus's push is rejected: Grace's commit reached the server first. Both changed the end of `menu.txt`, so integrating
will also conflict. On a team, working directly on `main` turns every push into a race.

## Fix

Linus integrates Grace's work (rebase his commit on top), resolves, and pushes:

```bash
git pull --rebase > /dev/null 2>&1 || true
printf 'espresso\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git add menu.txt && GIT_EDITOR=true git rebase --continue > /dev/null
git push -q
git log --oneline -3
```

```text
Successfully rebased and updated refs/heads/main.
2941d65 (HEAD -> main, origin/main, origin/HEAD) Add mocha
e8de87a Add chai
927a05a Merge remote-tracking branch 'origin/docs-hours'
```

Prevention: work on branches and merge through PRs (lesson 56), and protect `main` (lesson 59).
