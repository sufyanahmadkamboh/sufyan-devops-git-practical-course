<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 24 · Fast-forward merge · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

`--ff-only` when the branches have diverged:

```bash
git switch -q -c feature-mocha HEAD~1 && echo "mocha 3.90" >> prices.txt && git commit -q -am "Price mocha"
git switch -q main
git merge --ff-only feature-mocha 2>&1
```

```text
hint: Diverging branches can't be fast-forwarded, you need to either:
hint:
hint: 	git merge --no-ff
hint:
hint: or:
hint:
hint: 	git rebase
hint:
hint: Disable this message with "git config set advice.diverging false"
fatal: Not possible to fast-forward, aborting.
```

## Troubleshoot

`fatal: Not possible to fast-forward, aborting.`: `main` has a commit (`Add chai`) that `feature-mocha` does not, so
`main` cannot simply move forward to it. The branches have diverged:

```bash
git log --oneline --graph main feature-mocha | head -5
```

```text
* 45d6d00 (HEAD -> main, feature-chai) Add chai
| * 97d7b53 (feature-mocha) Price mocha
|/  
*   d986fad Merge branch 'feature-hours'
|\  
```

## Fix

Two valid choices: allow a merge commit (`git merge feature-mocha`), or first replay the branch on top of `main` so a
fast-forward becomes possible (rebase, lesson 61). With the rebase:

```bash
git switch -q feature-mocha
git rebase -q main
git switch -q main
git merge --ff-only feature-mocha
```

```text
Updating 45d6d00..8109406
Fast-forward
 prices.txt | 1 +
 1 file changed, 1 insertion(+)
```
