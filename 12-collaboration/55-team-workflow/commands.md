<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 55 · Team Git workflow · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-55 remote
cd ~/git-practice/lesson-55
git clone -q server/cafe.git linus
git -C linus config user.name "Linus Torvalds" && git -C linus config user.email "linus@example.com"
ls
```

## Demonstration

```bash
(cd ada && git switch -q -c feature-tea && echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q -u origin feature-tea)
(cd grace && git switch -q -c fix-latte-price && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price" && git push -q -u origin fix-latte-price)
(cd linus && git switch -q -c docs-hours && echo "Open 8-18" >> README.md && git commit -q -am "Document opening hours" && git push -q -u origin docs-hours)
git --git-dir=server/cafe.git branch
```

```bash
cd ada
git switch -q main && git fetch -q
for b in feature-tea fix-latte-price docs-hours; do git merge -q --no-ff --no-edit "origin/$b"; done
git push -q
git log --oneline --graph -8
```

```bash
cd ../linus && git switch -q main && git pull -q && git log --oneline -1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-55/grace
git branch
```

## Break it

```bash
cd ~/git-practice/lesson-55/grace && git pull -q
echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../linus && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

## Fix

```bash
git pull --rebase > /dev/null 2>&1 || true
printf 'espresso\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git add menu.txt && GIT_EDITOR=true git rebase --continue > /dev/null
git push -q
git log --oneline -3
```

## Practice challenge

```bash
cd ~/git-practice/lesson-55
for dev in ada grace linus; do
  git -C "$dev" fetch -q
  echo "$dev: $(git -C "$dev" rev-list --count main..origin/main) behind"
done
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-55
```
