<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 56 · Feature branch workflow · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-56 remote
cd ~/git-practice/lesson-56/ada
```

## Demonstration

```bash
git switch -q main && git pull -q
git switch -c feature/menu-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea to the menu"
git push -q -u origin feature/menu-tea
```

```bash
(cd ../grace && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price" && git push -q)
git fetch -q && git log --oneline -1 origin/main
```

```bash
git merge -q --no-edit origin/main
git log --oneline --graph -5
grep latte prices.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-56/ada
git push -q
for b in $(git branch -r --format='%(refname:short)' | grep feature/); do echo "$b $(git rev-list --count "$b..origin/main") behind"; done
```

## Break it

```bash
cd ~/git-practice/lesson-56/grace && git pull -q
git switch -q -c feature/new-prices
sed -i 's/espresso 2.50/espresso 2.70/; s/cappuccino 3.40/cappuccino 3.60/' prices.txt && git commit -q -am "New prices"
cd ../ada && git switch -q main && git merge -q feature/menu-tea && git pull -q --no-rebase --no-edit
for p in 2.55 2.60 2.65; do sed -i "s/^espresso .*/espresso $p/" prices.txt && git commit -q -am "Espresso $p" && git push -q; done
cd ../grace && git fetch -q && git merge origin/main 2>&1
```

## Troubleshoot

```bash
git rev-list --left-right --count HEAD...origin/main | awk '{print "branch has", $1, "own commit(s); main has", $2, "new commit(s)"}'
git merge --abort
```

## Fix

```bash
git merge origin/main > /dev/null 2>&1 || true
git checkout --ours prices.txt && git add prices.txt && git commit -q --no-edit
head -1 prices.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-56/ada
git fetch -q
git for-each-ref refs/remotes/origin --format='%(committerdate:unix) %(refname:short)' |
  awk -v limit="$(( $(date +%s) - 14*24*3600 ))" '$1 < limit {print $2}'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-56
```
