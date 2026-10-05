<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 97 · Releases · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-97 github
cd ~/git-practice/lesson-97
git log --oneline | tail -3
```

## Demonstration

```bash
git archive --format=tar.gz -o ../menu-v1.0.0.tar.gz 4267004 menu.txt prices.txt
gh release create v1.0.0 --target "$(git rev-parse 4267004)" --title "Cafe menu 1.0.0" \
  --notes "First published menu: espresso, latte, cappuccino, with prices." ../menu-v1.0.0.tar.gz
```

```bash
gh release create v1.1.0 --target main --title "Cafe menu 1.1.0" --notes "New drinks: green tea, chai and more."
```

```bash
git pull -q
awk 'NF == 2 {print $1 "," $2}' prices.txt > prices.csv && git rm -q prices.txt && git add prices.csv
git commit -q -m "feat!: prices as CSV (prices.txt removed)" && git push -q 2> /dev/null
gh release create v2.0.0 --target main --title "Cafe menu 2.0.0" \
  --notes "BREAKING: prices.txt is replaced by prices.csv (name,price). Update any tool that reads prices."
```

```bash
gh release list --limit 3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-97
mkdir -p ../lesson-97-download && gh release download v1.0.0 -D ../lesson-97-download --clobber
tar -xzf ../lesson-97-download/menu-v1.0.0.tar.gz -O prices.txt
```

## Break it

```bash
gh release create v1.1.0 --notes "New drinks: green tea and chai." 2>&1
```

## Fix

```bash
gh release edit v1.1.0 --notes "New drinks: green tea and chai." > /dev/null
gh release view v1.1.0 --json tagName,body --jq '"\(.tagName): \(.body)"'
```

## Practice challenge

```bash
cd ~/git-practice/lesson-97
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/releases/latest" --jq .tag_name
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-97 ~/git-practice/lesson-97-download ~/git-practice/menu-v1.0.0.tar.gz
```
