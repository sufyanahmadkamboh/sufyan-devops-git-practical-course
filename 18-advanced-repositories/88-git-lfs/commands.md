<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 88 · Git LFS · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-88 basic
cd ~/git-practice/lesson-88
git init -q --bare ../lesson-88-server.git && git remote add origin ../lesson-88-server.git
git lfs install --skip-repo > /dev/null
git lfs version | cut -d' ' -f1
```

## Demonstration

```bash
git lfs track "*.bin"
cat .gitattributes
```

```bash
head -c 2000000 /dev/zero | tr '\0' 'x' > menu-video.bin
git add .gitattributes menu-video.bin && git commit -q -m "Add the menu video"
git lfs ls-files
```

```bash
git cat-file -p HEAD:menu-video.bin
git cat-file -s HEAD:menu-video.bin
```

```bash
git push -q -u origin main 2>&1
echo "LFS objects on the server: $(find ../lesson-88-server.git/lfs/objects -type f | wc -l)"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-88-clone
wc -c < menu-video.bin
```

## Break it

```bash
cd ~/git-practice/lesson-88
head -c 3000000 /dev/zero | tr '\0' 'y' > dataset.csv
git add dataset.csv && git commit -q -m "Add the dataset"
git lfs track "*.csv" > /dev/null && git add .gitattributes && git commit -q -m "Track CSV files with LFS"
git cat-file -s HEAD:dataset.csv
```

## Troubleshoot

```bash
git lfs ls-files
```

## Fix

```bash
git lfs migrate import --yes --include="*.csv" --include-ref=main --exclude-ref=refs/remotes/origin/main > /dev/null 2>&1
git cat-file -s HEAD:dataset.csv
git lfs ls-files
```

## Practice challenge

```bash
cd ~/git-practice
GIT_LFS_SKIP_SMUDGE=1 git clone -q lesson-88-server.git lesson-88-light
head -c 120 lesson-88-light/menu-video.bin; echo
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-88 ~/git-practice/lesson-88-server.git ~/git-practice/lesson-88-clone ~/git-practice/lesson-88-light
```
