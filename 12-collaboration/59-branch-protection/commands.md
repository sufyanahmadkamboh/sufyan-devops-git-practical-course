<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 59 · Branch protection · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-59-gh github
```

```bash
bash scripts/new-lab.sh lesson-59 remote
cd ~/git-practice/lesson-59
```

## Demonstration

```bash
cat > server/cafe.git/hooks/pre-receive << 'EOF'
#!/usr/bin/env bash
# reject direct updates of main; changes arrive through merged pull requests (here: only the "pr-bot" may push main)
while read -r old new ref; do
  if [ "$ref" = "refs/heads/main" ] && [ "${PUSHER:-}" != "pr-bot" ]; then
    echo "error: main is protected: changes must be made through a pull request"
    exit 1
  fi
done
EOF
chmod +x server/cafe.git/hooks/pre-receive
ls server/cafe.git/hooks/ | grep -v sample
```

```bash
cd ada && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push 2>&1
```

```bash
git push -q origin HEAD:refs/heads/add-chai 2>&1
git reset -q --hard origin/main
cd ../grace && git fetch -q && git merge -q --ff-only origin/add-chai
PUSHER=pr-bot git push 2>&1
```

## Hands-on exercise

```bash
me=$(gh api user --jq .login)
printf '{"required_status_checks":null,"enforce_admins":true,"required_pull_request_reviews":{"required_approving_review_count":1},"restrictions":null,"allow_force_pushes":false,"allow_deletions":false}' |
  gh api -X PUT "repos/$me/git-practice-cafe/branches/main/protection" --input -
```

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches/main/protection" \
  --jq '"approvals: \(.required_pull_request_reviews.required_approving_review_count), enforce_admins: \(.enforce_admins.enabled)"'
```

## Break it

```bash
cd ~/git-practice/lesson-59-gh
echo "chai" >> menu.txt && git commit -q -am "Add chai directly"
git push 2>&1 | grep -E "remote: (error|-)|rejected|GH006" | head -4
test "${PIPESTATUS[0]}" -eq 0
```

## Fix

```bash
git switch -q -c add-chai-direct
git push -q -u origin add-chai-direct 2>&1 | grep -v "^remote:" || true
gh pr create --base main --title "Add chai" --body "Through a PR, as main is protected."
```

## Practice challenge

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/branches?protected=true" --jq '.[].name'
```

## Cleanup

```bash
cd ~/git-practice/lesson-59-gh
me=$(gh api user --jq .login)
gh pr close add-chai-direct --delete-branch > /dev/null 2>&1 || true
gh api -X DELETE "repos/$me/git-practice-cafe/branches/main/protection"
```

```bash
cd ~ && rm -rf ~/git-practice/lesson-59 ~/git-practice/lesson-59-gh
```
