<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 92 · Supply chain security · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-92 empty
cd ~/git-practice/lesson-92
git init -q --bare lib.git
git clone -q lib.git lib-author 2> /dev/null && cd lib-author
printf '#!/bin/sh\necho "deploying the cafe"\n' > deploy.sh && git add deploy.sh && git commit -q -m "Add deploy script"
git tag -a v1.0.0 -m "Release 1.0.0" && git push -q origin HEAD:main v1.0.0
cd .. && git clone -q --branch v1.0.0 lib.git consumer 2> /dev/null && sh consumer/deploy.sh
```

## Demonstration

```bash
cd lib-author
printf '#!/bin/sh\necho "deploying the cafe"\necho "(also sending your credentials somewhere)"\n' > deploy.sh
git commit -q -am "Improve logging"
git tag -f -a v1.0.0 -m "Release 1.0.0" > /dev/null
git push -f origin v1.0.0 2>&1 | grep -E "forced|v1.0.0"
```

```bash
cd .. && rm -rf consumer && git clone -q --branch v1.0.0 lib.git consumer 2> /dev/null
sh consumer/deploy.sh
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-92
sh pinned/deploy.sh
git -C pinned log --oneline -1
```

## Break it

```bash
cd ~/git-practice/lesson-92/lib-author
echo "# reviewed by Grace" >> deploy.sh
git -c user.name="Grace Hopper" -c user.email="grace@example.com" commit -q -am "Security fix"
git log -1 --format='%h %an <%ae> %s'
```

## Troubleshoot

```bash
git log -1 --format='%G? %an %s'
```

## Fix

```bash
git log --format='%G? %h %an %s' | awk '$1 != "G" {print "unsigned: " $0}'
```

## Practice challenge

```bash
git ls-remote https://github.com/actions/checkout refs/tags/v4 'refs/tags/v4^{}'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-92
```
