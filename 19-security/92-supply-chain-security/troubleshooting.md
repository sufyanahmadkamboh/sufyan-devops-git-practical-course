<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 92 · Supply chain security · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Authorship is not identity. Ada makes a commit claiming to be Grace, the maintainer everybody trusts:

```bash
cd ~/git-practice/lesson-92/lib-author
echo "# reviewed by Grace" >> deploy.sh
git -c user.name="Grace Hopper" -c user.email="grace@example.com" commit -q -am "Security fix"
git log -1 --format='%h %an <%ae> %s'
```

```text
bc42bcd Grace Hopper <grace@example.com> Security fix
```

## Troubleshoot

`git log` happily shows "Grace Hopper": author fields are free text. On GitHub, the commit would even show Grace's
avatar if her email is public. The only Git-level evidence is the **signature**, and this commit has none:

```bash
git log -1 --format='%G? %an %s'
```

```text
N Grace Hopper Security fix
```

`N` = no signature (`G` would be a good signature from a trusted key, lesson 91).

## Fix

Make unsigned or unverified commits stand out, and refuse them where it matters:

```bash
git log --format='%G? %h %an %s' | awk '$1 != "G" {print "unsigned: " $0}'
```

```text
unsigned: N bc42bcd Grace Hopper Security fix
unsigned: N 032597a Ada Lovelace Improve logging
unsigned: N 94faffe Ada Lovelace Add deploy script
```

On GitHub: branch protection "Require signed commits", "vigilant mode" (shows **Unverified** on commits that claim to
be you but are not signed by you), required reviews from CODEOWNERS, and 2FA (with passkeys or hardware keys) for every
account, so a stolen password alone cannot push.
