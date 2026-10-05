<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 11 · git commit · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-11 basic
cd ~/git-practice/lesson-11
```

## Demonstration

```bash
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add prices.txt
git commit -m "Raise the latte price to 3.30" -m "Milk prices went up 8 % this quarter."
```

```bash
git log -1
```

```bash
echo "green tea" >> menu.txt
echo "2 for 1 on Mondays" > specials.txt
git commit -q -a -m "Add green tea"
git status --short
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-11
git log -1 --format='%s%n%n%b'
git status --short
```

## Break it

```bash
echo "Open 8-18" > hours.txt
echo "Closed on public holidays" > holidays.txt
git add hours.txt
git commit -q -m "Add hte opening hours"
git log --oneline -1
```

## Fix

```bash
git add holidays.txt
git commit -q --amend -m "Add the opening hours"
git log --oneline -1
git show --stat --format= HEAD
```

## Practice challenge

```bash
cd ~/git-practice/lesson-11
echo "mocha" >> menu.txt && git add menu.txt
GIT_EDITOR='printf "Add a mocha\n\nCustomers asked for it.\nPrice follows tomorrow.\n" >' git commit -q
git log -1 --format='%s%n---%n%b'
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-11
```
