<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 43 · Upstream branches · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Create another branch and push it without `-u`:

```bash
git switch -q -c feature-mocha && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

```text
fatal: The current branch feature-mocha has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin feature-mocha

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```

## Troubleshoot

`fatal: The current branch feature-mocha has no upstream branch.`: Git does not know where to push this branch; it
does not assume a remote branch of the same name. The message prints the exact command to use.

## Fix

```bash
git push -q -u origin feature-mocha
git branch -vv | grep feature-mocha
```

```text
* feature-mocha f2833c1 [origin/feature-mocha] Add mocha
```

To never see the error again: `git config --global push.autoSetupRemote true`.
