# Glossary

The terms used in the course, in plain words, with the lesson that explains each one.

| Term | Meaning | Lesson |
|---|---|---|
| **annotated tag** | a tag object with tagger, date, message (and optional signature); used for releases | 69 |
| **bare repository** | a repository without a working directory (only the `.git` contents); what servers store | 37 |
| **bisect** | binary search through history for the commit that introduced a bug | 70 |
| **blame** | for each line of a file, the commit that last changed it | 71 |
| **blob** | the object that stores a file's content (no name, no permissions) | 74 |
| **branch** | a movable name (reference) pointing to a commit; moves forward with each commit | 17, 77 |
| **branch protection** | server rules for a branch: required PRs, reviews, checks; no force pushes | 59 |
| **checkout / switch** | change the current branch (and the files) | 19 |
| **cherry-pick** | apply the change of one commit onto the current branch as a new commit | 67 |
| **clone** | copy a whole repository (all history) and set up `origin` | 39 |
| **commit** | a snapshot of the project plus author, date, message and parent commit(s) | 11, 12 |
| **commit ID / hash / SHA** | the 40-character hash naming a commit (shortened to 7 in most outputs) | 12 |
| **conflict** | the same lines changed differently on both sides of a merge or rebase; Git asks you | 26 |
| **Conventional Commits** | message format `type(scope): description` (feat, fix, docs …), used for changelogs | 84 |
| **credential helper** | a program that stores and supplies HTTPS credentials (tokens) for Git | 48 |
| **default branch** | the branch a clone checks out and PRs target, usually `main` | 45 |
| **deploy key** | an SSH key registered on one repository, often read-only, for servers and CI | 49 |
| **detached HEAD** | `HEAD` points directly to a commit instead of a branch | 78 |
| **diff** | the line-by-line difference between two versions | 15 |
| **fast-forward** | a merge that only moves the branch label forward (no merge commit) | 24 |
| **fetch** | download new commits and update `origin/*`, without touching your branches | 40 |
| **force-with-lease** | a force push that refuses if someone else pushed in the meantime | 42 |
| **fork** | your own server-side copy of someone else's repository | 38 |
| **gitignore** | patterns of files Git should not track (`.gitignore`) | 73 |
| **Git LFS** | Large File Storage: big files stored outside Git, pointers inside | 88 |
| **GitHub Actions** | GitHub's CI/CD: workflows in `.github/workflows/` run on events such as push | 98 |
| **HEAD** | "where you are": normally points to the current branch | 76 |
| **hook** | a script Git runs automatically at an event (pre-commit, commit-msg, pre-push …) | 82 |
| **index / staging area** | the list of what goes into the next commit | 10 |
| **interactive rebase** | `git rebase -i`: reorder, reword, edit, squash, fixup or drop commits | 63 |
| **issue** | a GitHub item tracking a bug, task or request; closed by `Fixes #N` | 93 |
| **label** | a tag on issues and PRs: type, priority, area | 94 |
| **merge** | combine another branch into the current one | 23 |
| **merge base** | the most recent commit two branches share; the base of a three-way merge | 25 |
| **merge commit** | a commit with two (or more) parents | 23 |
| **milestone** | a group of issues/PRs with a goal and due date, often a release | 95 |
| **object** | blob, tree, commit or tag in `.git/objects`, named by the hash of its content | 74 |
| **ORIG_HEAD** | where HEAD was before the last reset, merge or rebase | 31 |
| **origin** | the default name of the remote you cloned from | 37 |
| **origin/main** | a remote-tracking branch: your clone's memory of the server's `main` | 37 |
| **personal access token** | a credential used instead of a password for Git over HTTPS and the API | 48 |
| **pull** | fetch + integrate (merge or rebase) into the current branch | 41 |
| **pull request (PR)** | a request to merge a branch, with diff, discussion, review and checks | 51 |
| **push** | upload commits and move the branch on the server (fast-forward only) | 42 |
| **rebase** | replay commits on top of another commit, creating new commits | 60 |
| **reflog** | local log of every position of HEAD and branches; the recovery tool | 33 |
| **release** | a GitHub page for a tag with notes and downloadable assets | 97 |
| **remote** | a named URL of another copy of the repository | 37 |
| **reset** | move the current branch to another commit (`--soft`, `--mixed`, `--hard`) | 31 |
| **restore** | discard working-directory changes or unstage (`--staged`) | 29, 30 |
| **revert** | a new commit that undoes an earlier one (safe for shared history) | 32 |
| **semantic versioning** | MAJOR.MINOR.PATCH: breaking / feature / fix | 97 |
| **signed commit** | a commit with a GPG or SSH signature proving who made it | 91 |
| **squash** | combine several commits into one (interactive rebase, or squash merge) | 54, 63 |
| **stash** | a shelf for uncommitted changes (`git stash`, `pop`, `apply`) | 34 |
| **submodule** | another repository embedded at a pinned commit | 86 |
| **supply chain** | everything your software is built from: dependencies, actions, images, their authors | 92 |
| **tag** | a fixed name for a commit, usually a version | 68 |
| **three-way merge** | a merge that compares both tips with their merge base | 25 |
| **tree** | the object for a folder: names, modes and the blob/tree IDs | 74 |
| **upstream** | the remote branch a local branch tracks (for push, pull, ahead/behind) | 43 |
| **working directory** | the files you see and edit | 07 |
| **worktree** | an additional working directory of the same repository, on another branch | 87 |
