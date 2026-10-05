# Lesson 68 · Git tags

> Level 14 · Advanced Git · ⏱ 15 minutes

## What are we learning?

A tag is a name fixed to one commit, usually a version: `v1.0.0`. Unlike a branch, it does not move when you commit.
We create tags, list them, check one out, and push them (tags are **not** pushed with branches).

## Visual

```text
 A ── B ── C ── D ── E   ← main (moves with every commit)
           ▲         ▲
        v1.0.0     v1.1.0          (tags stay where they were created)
```

## Lab setup

<!-- test: contains=lesson-68 -->
```bash
bash scripts/new-lab.sh lesson-68 remote
cd ~/git-practice/lesson-68/ada
git log --oneline
```

## Demonstration

Tag the current commit as the first release, and an older commit as a pre-release:

<!-- test: contains=v1.0.0; output -->
```bash
git tag v1.0.0
git tag v0.9.0 fc345e6
git tag
git log --oneline --decorate
```

```text
v0.9.0
v1.0.0
4267004 (HEAD -> main, tag: v1.0.0, origin/main, origin/HEAD) Add prices
fc345e6 (tag: v0.9.0) Add the menu
d6df412 Add README
```

Work continues; the tag stays:

<!-- test: contains=tag: v1.0.0; output -->
```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --decorate -2
```

```text
a13f24c (HEAD -> main) Add green tea
4267004 (tag: v1.0.0, origin/main, origin/HEAD) Add prices
```

Look at the code of a release (a detached HEAD, lesson 78: look, do not commit):

<!-- test: absent=green tea; output -->
```bash
git switch -q --detach v1.0.0
cat menu.txt
git switch -q main
```

```text
espresso
latte
cappuccino
```

## Command breakdown

| Command | What it does |
|---|---|
| `git tag NAME [COMMIT]` | lightweight tag on HEAD (or COMMIT) |
| `git tag` / `git tag -l "v1.*"` | list (with a pattern) |
| `git push origin NAME` | push one tag |
| `git push --tags` / `git push --follow-tags` | push all tags / annotated tags reachable from pushed commits |
| `git tag -d NAME` / `git push origin --delete NAME` | delete locally / on the server |
| `git ls-remote --tags origin` | tags on the server |

## Hands-on exercise

**Instructions.** List the tags matching `v1.*` and show which commit `v0.9.0` points to.

**Expected result.** `v1.0.0`; `fc345e6 (tag: v0.9.0) Add the menu`.

**Verification.**

<!-- test: contains=v0.9.0) Add the menu -->
```bash
cd ~/git-practice/lesson-68/ada
git tag -l "v1.*"
git log --oneline -1 v0.9.0
```

## Break it

Push the branch and expect the tags on the server:

<!-- test: contains=no tags on the server; output -->
```bash
git push -q
git ls-remote --tags origin | grep . || echo "no tags on the server"
```

```text
no tags on the server
```

## Troubleshoot

`git push` sends branches, not tags. Grace, cloning or fetching from the server, would not see `v1.0.0`, and a CI job
triggered "on tag push" would never run.

## Fix

<!-- test: contains=[new tag]; output -->
```bash
git push origin v1.0.0 2>&1
git ls-remote --tags origin
```

```text
To ~/git-practice/lesson-68/server/cafe.git
 * [new tag]         v1.0.0 -> v1.0.0
4267004871ae95e12690719f02460f9e3c935cf5	refs/tags/v1.0.0
```

(`git push --tags` would also push `v0.9.0`; push the tags you mean to publish.)

## Real-world example

Releases are tags. A CI workflow `on: push: tags: ['v*']` builds the release artifacts when `v1.4.0` is pushed; the
Helm chart's `appVersion` and the Docker image tag use the same version. Tags are also what `git describe` uses to
name a build (lesson 69) and what GitHub Releases are attached to (lesson 97).

## Practice challenge

Tag a mistake, `v1.0.1` on the wrong commit, then delete it locally before anyone sees it.

<details>
<summary>Solution</summary>

<!-- test: contains=Deleted tag 'v1.0.1'; output -->
```bash
cd ~/git-practice/lesson-68/ada
git tag v1.0.1 d6df412
git tag -d v1.0.1
git tag
```

```text
Deleted tag 'v1.0.1' (was d6df412)
v0.9.0
v1.0.0
```

Once a tag is pushed and others have fetched it, deleting or moving it causes confusion: publish a new version instead.

</details>

## Recap

- A tag names a commit permanently; branches move, tags do not.
- Tags must be pushed explicitly: `git push origin TAG`.
- Check out a tag to inspect a release (detached HEAD); never move published tags.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-68
```

Next: [Lesson 69 · Annotated tags](../69-annotated-tags/README.md).
