# Lesson 97 · Releases

> Level 20 · GitHub advanced · ⏱ 25 minutes

## What are we learning?

A GitHub Release is a tag (lesson 68) plus a page: title, release notes, and downloadable files (binaries, archives,
checksums). We publish three versions of the cafe menu, **v1.0.0**, **v1.1.0** and **v2.0.0**, following semantic
versioning, with generated notes and an attached asset.

## Visual

```text
 semantic versioning  MAJOR.MINOR.PATCH
   v1.0.0  first release
   v1.1.0  new things, nothing broken          (feat)
   v2.0.0  something incompatible changed      (feat! / BREAKING CHANGE)
   v2.0.1  bug fix only                        (fix)

 gh release create v1.1.0 --target <commit> --title … --generate-notes  menu.tar.gz
   └── tag v1.1.0 (created if missing) + release page + notes from merged PRs + asset
```

## Lab setup

<!-- test: github; contains=lesson-97 -->
```bash
bash scripts/new-lab.sh lesson-97 github
cd ~/git-practice/lesson-97
git log --oneline | tail -3
```

<!-- test-run github: gh auth setup-git -->
<!-- test-run github: cd ~/git-practice/lesson-97 && for v in v1.0.0 v1.1.0 v2.0.0; do gh release delete "$v" --yes --cleanup-tag > /dev/null 2>&1 || true; git push -q origin --delete "refs/tags/$v" > /dev/null 2>&1 || true; done -->
<!-- test-run github: cd ~/git-practice/lesson-97 && if [ -f prices.csv ]; then git rm -q prices.csv && git show 4267004:prices.txt > prices.txt && git add prices.txt && git commit -q -m "test: restore prices.txt for the lessons" && git push -q 2> /dev/null; fi -->

The practice repository's first commits (`d6df412` … `4267004`) are the same as in every lab; later commits come from
the earlier GitHub lessons.

## Demonstration

**v1.0.0** on the commit that completed the first menu with prices, with the menu as a downloadable archive
(`--target` takes a branch name or a **full** commit ID):

<!-- test: github; contains=/releases/tag/v1.0.0; output -->
```bash
git archive --format=tar.gz -o ../menu-v1.0.0.tar.gz 4267004 menu.txt prices.txt
gh release create v1.0.0 --target "$(git rev-parse 4267004)" --title "Cafe menu 1.0.0" \
  --notes "First published menu: espresso, latte, cappuccino, with prices." ../menu-v1.0.0.tar.gz
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/releases/tag/v1.0.0
```

**v1.1.0**: new drinks were added since (a minor version), on the current `main`:

<!-- test: github; contains=/releases/tag/v1.1.0; output -->
```bash
gh release create v1.1.0 --target main --title "Cafe menu 1.1.0" --notes "New drinks: green tea, chai and more."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/releases/tag/v1.1.0
```

**v2.0.0**: an incompatible change, the price file format becomes CSV; tools reading the old format break, so the
major version changes:

<!-- test: github; contains=/releases/tag/v2.0.0; output -->
```bash
git pull -q
awk 'NF == 2 {print $1 "," $2}' prices.txt > prices.csv && git rm -q prices.txt && git add prices.csv
git commit -q -m "feat!: prices as CSV (prices.txt removed)" && git push -q 2> /dev/null
gh release create v2.0.0 --target main --title "Cafe menu 2.0.0" \
  --notes "BREAKING: prices.txt is replaced by prices.csv (name,price). Update any tool that reads prices."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/releases/tag/v2.0.0
```

<!-- test: github; retry=10; contains=v2.0.0; output -->
```bash
gh release list --limit 3
```

```text
Cafe menu 2.0.0	Latest	v2.0.0	2026-10-05T02:17:14Z
Cafe menu 1.1.0		v1.1.0	2026-10-05T02:17:11Z
Cafe menu 1.0.0		v1.0.0	2026-10-05T02:17:10Z
```

## Command breakdown

| Command | What it does |
|---|---|
| `gh release create TAG [FILES] --target REV --title T --notes N` | publish (creates the tag if missing) |
| `--generate-notes` | notes from merged PRs and contributors since the previous release |
| `--prerelease` / `--draft` / `--latest=false` | mark as pre-release / keep unpublished / not "Latest" |
| `gh release list` / `view TAG` | releases / one release |
| `gh release upload TAG FILE` / `download TAG` | add / fetch assets |
| `gh release edit TAG --notes …` | change a release |
| `gh release delete TAG --cleanup-tag` | delete it and its tag |

## Hands-on exercise

**Instructions.** Download v1.0.0's asset into a new folder and check its contents.

**Expected result.** `menu.txt` and `prices.txt` with the 1.0.0 prices.

**Verification.**

<!-- test: github; contains=latte 3.20 -->
```bash
cd ~/git-practice/lesson-97
mkdir -p ../lesson-97-download && gh release download v1.0.0 -D ../lesson-97-download --clobber
tar -xzf ../lesson-97-download/menu-v1.0.0.tar.gz -O prices.txt
```

## Break it

Publish v1.1.0 again with corrected notes:

<!-- test: github; fail; contains=already exists; output -->
```bash
gh release create v1.1.0 --notes "New drinks: green tea and chai." 2>&1
```

```text
HTTP 422: Validation Failed (https://api.github.com/repos/sufyanahmadkamboh/git-practice-cafe/releases)
Release.tag_name already exists
```

## Troubleshoot

A tag can have one release, and a published version number must never be reused for different content (users,
caches and lock files already refer to it). Changing the **text** of a release is fine; changing its **code** means a
new version.

## Fix

<!-- test: github; contains=green tea and chai; output -->
```bash
gh release edit v1.1.0 --notes "New drinks: green tea and chai." > /dev/null
gh release view v1.1.0 --json tagName,body --jq '"\(.tagName): \(.body)"'
```

```text
v1.1.0: New drinks: green tea and chai.
```

## Real-world example

Release pipelines: pushing a `v*` tag triggers a workflow that builds binaries for each platform, signs them, writes
checksums, generates notes from Conventional Commits (lesson 84), and runs `gh release create` with the artifacts;
Docker images and Helm charts are published with the same version. The release page becomes the single place where
users find what changed and download it.

## Practice challenge

Which release does GitHub mark as **Latest**, and why not v1.1.0 even though it was edited last?

<details>
<summary>Solution</summary>

<!-- test: github; contains=v2.0.0; output -->
```bash
cd ~/git-practice/lesson-97
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/releases/latest" --jq .tag_name
```

```text
v2.0.0
```

"Latest" is the highest semantic version among non-prerelease releases by default, not the most recently edited.

</details>

## Recap

- Release = tag + notes + assets; versions follow MAJOR.MINOR.PATCH.
- `gh release create/list/view/edit/delete`; `--generate-notes` for automatic notes.
- Never reuse a version for different content: edit notes, release new versions.

## Cleanup

The releases stay on the practice repository as an example (delete them with `gh release delete TAG --cleanup-tag`).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-97 ~/git-practice/lesson-97-download ~/git-practice/menu-v1.0.0.tar.gz
```

Next: [Lesson 98 · GitHub Actions introduction](../98-github-actions-intro/README.md).
