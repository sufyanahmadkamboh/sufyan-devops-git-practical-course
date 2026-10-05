# Interview questions

Questions DevOps and platform engineers are asked about Git and GitHub, with the answers the course builds. Each answer
names the lesson where you practised it; the best interview answers add a short "in my last project…" example.

## Fundamentals

**1. What is the difference between Git and GitHub?**
Git is the version-control tool that runs on your computer and stores history in `.git`. GitHub is a hosting and
collaboration service built around Git repositories: remotes, pull requests, reviews, Actions, releases. (Lessons 01–02, 44)

**2. What are the working directory, the staging area and the repository?**
The files you edit; the list of changes chosen for the next commit (`git add`); the committed history in `.git`.
`git status` compares them. (Lessons 07–10)

**3. What is a commit, exactly?**
An object containing a tree (the snapshot), the parent commit ID(s), author, committer and message. Its ID is the hash
of all of that, so changing anything creates a different commit. (Lessons 12, 74–75)

**4. Why does a commit ID change after `--amend` even if the files are identical?**
The committer date (and possibly message) changes, and the ID is a hash of the whole commit object. (Lesson 12)

## Branching and merging

**5. What is a branch in Git?**
A reference: a small file containing one commit ID. Creating it is instant; committing moves it. (Lessons 17, 77)

**6. Fast-forward vs three-way merge?**
Fast-forward: the current branch has not moved, so its label moves forward, no merge commit. Three-way: both moved;
Git compares both tips with their merge base and creates a merge commit with two parents. (Lessons 24–25)

**7. How do you resolve a merge conflict?**
Read `git status`, open the file, decide the correct content (talk to the other author if needed), remove all
markers, `git add`, `git commit`; run the tests before pushing. `git merge --abort` if you need to step back. (Lessons 26–28)

**8. Merge vs rebase: when do you use which?**
Rebase your own unshared branch onto `main` to keep a linear history; merge (or squash-merge via PR) to integrate into
shared branches. Never rebase commits others have built on. (Lessons 60–62)

**9. What do squash, merge commit and rebase merge do on GitHub?**
Squash: one new commit per PR. Merge commit: all commits plus a merge commit. Rebase merge: all commits replayed
linearly, no merge commit. Each leaves a different history on `main`. (Lesson 54)

## Undoing and recovery

**10. `reset --soft`, `--mixed`, `--hard`?**
All move the branch. Soft keeps changes staged; mixed (default) keeps them unstaged; hard discards them from the
staging area and working directory. (Lesson 31)

**11. `reset` vs `revert`?**
Reset rewrites the branch (local, unpushed work). Revert adds a new commit undoing an old one: the only safe way on a
shared branch. A merge is reverted with `-m 1`. (Lessons 31–32)

**12. You ran `git reset --hard` by mistake. Can you recover?**
Committed work: yes, with `git reflog` or `ORIG_HEAD`. Staged-only work: often, with `git fsck --lost-found` (dangling
blobs). Never-staged edits: no. (Lessons 33, 81)

**13. Someone deleted a branch on GitHub. How do you get it back?**
"Restore branch" on its last PR; or from any clone that still has `origin/NAME`; or your reflog if you worked on it;
then push it back. (Lesson 79)

**14. What is detached HEAD and is it dangerous?**
HEAD points at a commit, not a branch: normal when inspecting a tag or in CI. Commits made there belong to no branch;
create a branch before leaving (`git switch -c`). (Lesson 78)

## Remotes and collaboration

**15. `fetch` vs `pull`?**
Fetch downloads and updates `origin/*` only. Pull = fetch + merge or rebase into the current branch. Fetch first when
you want to look before integrating. (Lessons 40–41)

**16. Your push is rejected with "fetch first". What happened and what do you do?**
Someone pushed to the branch; the server's branch has commits you lack. Pull (preferably `--rebase`), resolve if
needed, push again. Not `--force`. (Lesson 42, troubleshooting 8)

**17. When is `--force-with-lease` appropriate?**
After rewriting your own feature branch (rebase, amend); it refuses if someone else pushed meanwhile, unlike `--force`.
Never on `main`. (Lessons 42, 60)

**18. What is an upstream branch?**
The remote branch a local branch tracks; it enables plain `git push`/`git pull` and ahead/behind counts. Set with
`git push -u`. (Lesson 43)

**19. Describe GitHub Flow and Git Flow. Which do you prefer?**
GitHub Flow: `main` always deployable, short branches, PRs, deploy on merge, ideal for continuously deployed services.
Git Flow: `develop`, release and hotfix branches, useful for versioned products maintained in parallel; often too heavy
for web services. (Lessons 57–58)

**20. How do you enforce code review and CI?**
Branch protection on `main`: PRs required, approvals (often via CODEOWNERS), required status checks up to date,
enforced for admins, no force pushes. (Lesson 59)

## Advanced Git

**21. How would you find which commit introduced a bug?**
`git bisect start BAD GOOD`, then `git bisect run ./test.sh` (exit 0 good, 1 bad, 125 skip). (Lesson 70)

**22. How do you get a fix from `main` into a release branch?**
`git cherry-pick -x SHA` on the release branch, tag a patch release. Cherry-pick dependencies first if the fix builds
on them. (Lessons 67, project 5)

**23. Lightweight vs annotated tags?**
Lightweight: just a name. Annotated: an object with tagger, date, message, optional signature; required by
`git describe` and best for releases. (Lessons 68–69)

**24. What are Git hooks and how do teams share them?**
Scripts run at events (pre-commit, commit-msg, pre-push; pre-receive on servers). They are not cloned: teams commit
them and set `core.hooksPath`, or use the pre-commit framework, and enforce the same checks in CI. (Lessons 82–85)

**25. Submodules, worktrees, LFS: one sentence each.**
A submodule embeds another repository pinned to a commit; a worktree is another working directory of the same
repository on another branch; LFS stores large binaries outside Git behind pointer files. (Lessons 86–88)

## Internals

**26. Name Git's object types.**
Blob (content), tree (folder), commit (snapshot + history), tag (annotated tag). All named by the hash of their
content. (Lessons 74–75)

**27. What does `git add` actually do?**
Writes the file's content as a blob into the object store and records it in the index; `git commit` then writes a
tree from the index, a commit object, and moves the branch. (Lesson 75)

## Security

**28. A secret was committed and pushed. What do you do?**
Revoke or rotate it immediately (that is the fix); check access logs; then remove it from history with `git filter-repo`
on a mirror clone, force-push, have everyone re-clone, ask GitHub to purge caches; prevent with `.gitignore`, scanners,
push protection. (Lessons 89–90, troubleshooting 12)

**29. Why does `git rm` not remove a secret?**
It only removes the file from the next snapshot; every earlier commit still contains it, in every clone. (Lesson 89)

**30. Why sign commits, and how?**
Author fields are free text; a signature proves possession of a key. `gpg.format ssh`, `user.signingkey`,
`commit.gpgsign true`, an allowed signers file for verification; GitHub shows Verified with the uploaded key. (Lesson 91)

**31. What supply-chain risks exist around Git and GitHub Actions?**
Mutable tags and branches (pin actions by commit SHA), spoofed authors (require signatures), compromised accounts (2FA,
least-privilege tokens), malicious commits in large changes (review, CODEOWNERS). (Lesson 92)

## DevOps

**32. Describe a release process you would build with Git.**
Conventional Commits, PRs into protected `main`, CI on every PR, an annotated semver tag triggers the release workflow:
image to a registry, chart or artifacts to a release, deployment with Helm or GitOps; rollback = redeploy the previous
tag. (Module 21, capstone)

**33. How do you keep a long-running feature branch from becoming a merge nightmare?**
Merge or rebase `main` into it often, keep it short, split it into smaller PRs, use feature flags to merge unfinished
work safely. (Lesson 56)

**34. A deployment from tag `v1.2.0` fails because its image does not exist. How do you investigate and recover?**
`kubectl describe` / events show the pull error; the tag exists in Git but the image was never built. Roll back
(`helm rollback`, or deploy the previous tag), then fix the pipeline so tags always build before deploying. (Project 6)

**35. Why does CI fail with "no tag exactly matches" or an empty changelog?**
A shallow clone (`fetch-depth: 1`) has no tags or history; set `fetch-depth: 0` for release jobs. (Lessons 39, 69)
