<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 70 · Git bisect · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Mark the commits the wrong way round:

```bash
git bisect start
git bisect good HEAD
git bisect bad "$(git rev-list --max-parents=0 HEAD)" 2>&1
```

```text
status: waiting for both good and bad commits
status: waiting for bad commit, 1 good commit known
Some good revs are not ancestors of the bad rev.
git bisect cannot work properly in this case.
Maybe you mistook good and bad revs?
```

## Troubleshoot

`Some good revs are not ancestors of the bad rev … Maybe you mistook good and bad revs?`: bisect searches for the
commit where things went from good to bad, so the good commit must be older than the bad one. Here it is reversed.

## Fix

Start over with the right order:

```bash
git bisect reset > /dev/null 2>&1
git bisect start HEAD "$(git rev-list --max-parents=0 HEAD)" > /dev/null
git bisect run bash check.sh 2>&1 | grep "is the first bad commit"
git bisect reset > /dev/null 2>&1
```

```text
3ceea031d6f34d67cc8f33c993ea0784c54ae95f is the first bad commit
```

(If you are looking for when something was **fixed**, use other words: `git bisect start --term-old=broken
--term-new=fixed`.)
