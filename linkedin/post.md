Most Git tutorials stop at add, commit, push. Then real work begins: a merge conflict before a release, a push rejected because a colleague was faster, a "git reset --hard" that just ate three commits, a password that slipped into the history. So I built a free, hands-on Git course that teaches exactly those moments. 🌿👇

Think of Git as a time machine for a folder, with a logbook. Every lesson teaches one control of the machine, and then breaks it on purpose so you learn to read the dials when something goes wrong.

That is the "Git Practical Course: Git & GitHub From Beginner to Advanced":

📚 98 lessons, from your first commit to interactive rebase, recovery, hooks, signing and supply-chain security
🔀 pull requests, reviews, branch protection, issues, releases and GitHub Actions, practised on a real GitHub repository
🧯 18 troubleshooting labs: Problem → Symptoms → Investigation → Root cause → Fix → Verification → Prevention
🏗️ 6 projects and a capstone: a broken repository turned into a protected GitHub repository whose v1.0.0 tag builds an image, pushes it to GHCR and deploys it with Helm to Kubernetes

Every lesson follows the same path: Understand → Visualize → Execute → Observe → Break → Troubleshoot → Fix → Practice → Challenge → Real world.

Things I learned while building and testing it:
🔹 committed work is almost never lost: "git reflog" remembers every position of HEAD; only edits you never staged are really gone
🔹 even staged-but-uncommitted files survive a hard reset, as dangling blobs that "git fsck --lost-found" recovers
🔹 a rebase skips commits that are already upstream by patch, which is how you repair a branch someone rebased under you
🔹 "git rm" does not remove a secret: it stays in every earlier commit, in every clone; rotate first, then rewrite history
🔹 Git tags and action versions are mutable: pin GitHub Actions to a commit SHA

✅ Every lesson is also a test: 1,308 code blocks run automatically in GitHub Actions with the latest Git, in a sandbox, and the outputs in the lessons are the real outputs. The 153 blocks that need GitHub ran against GitHub itself: pull requests, reviews, protection rules, issues, releases and Actions runs.

Also included: an assessment per module, a command reference lab, a final exam with a separate solution, a 23-video series (3 h 24 min in total, full and silent versions), a 125-page study guide PDF, a glossary and 35 interview questions.

🔗 Repository: https://github.com/sufyanahmadkamboh/sufyan-devops-git-practical-course
🌐 All my projects: https://sufyanahmadkamboh.github.io/

Which Git error cost you the most time? 💬

#Git #GitHub #DevOps #GitHubActions #SoftwareEngineering #VersionControl #LearningDevOps #OpenSource
