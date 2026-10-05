<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 59 · Branch protection · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Push directly to the protected `main` on GitHub, even as the repository's owner:

```bash
cd ~/git-practice/lesson-59-gh
echo "chai" >> menu.txt && git commit -q -am "Add chai directly"
git push 2>&1 | grep -E "remote: (error|-)|rejected|GH006" | head -4
test "${PIPESTATUS[0]}" -eq 0
```

```text
remote: error: GH006: Protected branch update failed for refs/heads/main.        
remote: - Changes must be made through a pull request.        
 ! [remote rejected] main -> main (protected branch hook declined)
```

## Troubleshoot

`GH006: Protected branch update failed for refs/heads/main` and `Changes must be made through a pull request`: the
rule works, including for the owner (enforced for admins). Nothing changed on GitHub; the commit is only local.

## Fix

The commit belongs on a branch with a PR:

```bash
git switch -q -c add-chai-direct
git push -q -u origin add-chai-direct 2>&1 | grep -v "^remote:" || true
gh pr create --base main --title "Add chai" --body "Through a PR, as main is protected."
```

```text
https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/13
```

The PR now needs one approval from someone else before it can be merged (on a solo practice repository, nobody can:
the rule is doing its job).
