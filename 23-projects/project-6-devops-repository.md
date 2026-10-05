# Project 6 · DevOps repository

> Level 24 · Projects · advanced · ⏱ 2 hours · module 21, lessons 56, 68–69, 97–98 · needs Docker, kind, Helm, kubectl

## Brief

Run the module 21 repository for real: Git tags decide what is deployed. Each release tag is built into a container
image, loaded into a local Kubernetes cluster (kind), and deployed with the repository's Helm chart. Then a release
goes wrong in production and you roll back.

This project connects the series: containers from
[Docker from zero](https://github.com/sufyanahmadkamboh/sufyan-devops-docker-from-zero), clusters from
[Kubernetes from zero](https://github.com/sufyanahmadkamboh/sufyan-devops-kubernetes-from-zero), charts from
[Helm from zero](https://github.com/sufyanahmadkamboh/sufyan-devops-helm-from-zero), and Git from this course.

```text
 git tag v1.1.0 ──► git switch --detach v1.1.0 ──► docker build -t cafe:1.1.0 ──► kind load ──► helm upgrade --set image.tag=1.1.0
                                                                                                      │
                                                         rollback = helm rollback / redeploy the previous tag
```

## Requirements

1. The repository from module 21's template, with `v1.0.0` and `v1.1.0` (chai added on a feature branch, released with
   `scripts/release.sh`).
2. A kind cluster `git-course`; each deployed version's image is built **from its tag**, not from the working tree.
3. `v1.0.0` deployed, then upgraded to `v1.1.0`; the running pods serve chai.
4. A broken deployment (`1.2.0` released in Git, but no image built) is detected and rolled back to `1.1.0`.
5. Helm's history shows every deployment and the rollback.

## Starting point

<!-- test: contains=v1.0.0 -->
```bash
bash scripts/new-lab.sh project-6 empty
cp -r 21-devops-workflow/devops-project/. ~/git-practice/project-6/
cd ~/git-practice/project-6
git add . && git commit -q -m "chore: initial cafe DevOps repository"
git tag -a v1.0.0 -m "Release 1.0.0"
git log --oneline --decorate
```

<!-- test-run: kind delete cluster --name git-course > /dev/null 2>&1 || true -->

A local Kubernetes cluster (a minute or two the first time):

<!-- test: timeout=600; contains=kind-git-course; output -->
```bash
kind create cluster --name git-course --wait 120s > /dev/null 2>&1
kubectl config current-context
kubectl get nodes
```

```text
kind-git-course
NAME                       STATUS   ROLES           AGE   VERSION
git-course-control-plane   Ready    control-plane   23s   v1.37.0
```

## Hints

- Build from a tag without touching your working tree: `git worktree add ../build-v1.0.0 v1.0.0` (lesson 87), or
  `git archive v1.0.0 | docker build -t cafe:1.0.0 -` (the tag's exact files as the build context).
- `kind load docker-image cafe:1.0.0 --name git-course` makes a local image available to the cluster.
- `helm upgrade --install cafe helm/cafe --set image.repository=cafe --set image.tag=X --wait`.

## Reference solution

<details>
<summary>Show the reference solution</summary>

A helper that deploys a tag: build the tag's files, load the image, upgrade the release:

<!-- test: contains=deploy-tag -->
```bash
cd ~/git-practice/project-6
cat > ../deploy-tag.sh << 'EOF'
#!/usr/bin/env bash
# deploy-tag.sh TAG: build the image from the tag's files, load it into kind, deploy it with the tag's chart
set -euo pipefail
tag=$1; version=${tag#v}
git archive "$tag" | docker build -q -t "cafe:$version" - > /dev/null
kind load docker-image "cafe:$version" --name git-course > /dev/null 2>&1
rm -rf "../chart-$version" && mkdir "../chart-$version" && git archive "$tag" helm | tar -x -C "../chart-$version"
helm upgrade --install cafe "../chart-$version/helm/cafe" --set image.repository=cafe --set image.tag="$version" \
  --wait --timeout 180s > /dev/null
echo "deployed $tag"
EOF
echo "deploy-tag.sh ready"
```

Deploy v1.0.0:

<!-- test: timeout=600; contains=deployed v1.0.0; output -->
```bash
bash ../deploy-tag.sh v1.0.0
kubectl get deploy cafe
kubectl exec deploy/cafe -- wget -qO- http://127.0.0.1:8080/menu.json | grep -c '"name"'
```

```text
deployed v1.0.0
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
cafe   2/2     2            2           2s
3
```

A feature through Git, released as v1.1.0, deployed:

<!-- test: timeout=600; contains=chai; output -->
```bash
git switch -q -c feat/add-chai
sed -i 's/{"name": "cappuccino", "price": "3.40"}/{"name": "cappuccino", "price": "3.40"},\n    {"name": "chai", "price": "3.10"}/' application/menu.json
git commit -q -am "feat(menu): add chai"
git switch -q main && git merge -q --no-ff -m "Merge branch 'feat/add-chai'" feat/add-chai
bash scripts/release.sh 1.1.0
bash ../deploy-tag.sh v1.1.0
kubectl exec deploy/cafe -- wget -qO- http://127.0.0.1:8080/menu.json | grep chai
```

```text
released v1.1.0: push with  git push --follow-tags
deployed v1.1.0
    {"name": "chai", "price": "3.10"}
```

The break: `1.2.0` is released in Git, but the image is never built; the deployment cannot start and Helm gives up:

<!-- test: timeout=300; fail; contains=context deadline exceeded; output -->
```bash
bash scripts/release.sh 1.2.0 > /dev/null
helm upgrade cafe helm/cafe --set image.repository=cafe --set image.tag=1.2.0 --wait --timeout 60s 2>&1 | tail -1
test "${PIPESTATUS[0]}" -eq 0
```

```text
context deadline exceeded
```

Investigate, then roll back to the last good release:

<!-- test: contains=ErrImage; output -->
```bash
kubectl get pods -l app.kubernetes.io/name=cafe -o custom-columns='POD:.metadata.name,IMAGE:.spec.containers[0].image,STATUS:.status.containerStatuses[0].state.waiting.reason' | grep 1.2.0 | sed -E 's/cafe-[a-z0-9]+-[a-z0-9]+/cafe-…/'
```

```text
cafe-…   cafe:1.2.0   ErrImagePull
```

<!-- test: timeout=300; contains=chai; output -->
```bash
helm rollback cafe 2 --wait --timeout 120s
helm history cafe --max 4
kubectl exec deploy/cafe -- wget -qO- http://127.0.0.1:8080/menu.json | grep chai
```

```text
Rollback was a success! Happy Helming!
REVISION	UPDATED                 	STATUS    	CHART     	APP VERSION	DESCRIPTION                                                                                                 
1       	Mon Oct  5 04:31:33 2026	superseded	cafe-1.0.0	1.0.0      	Install complete                                                                                            
2       	Mon Oct  5 04:31:39 2026	superseded	cafe-1.1.0	1.1.0      	Upgrade complete                                                                                            
3       	Mon Oct  5 04:31:43 2026	failed    	cafe-1.2.0	1.2.0      	Upgrade "cafe" failed: resource Deployment/default/cafe not ready. status: InProgress, message: Updated: ...
4       	Mon Oct  5 04:32:43 2026	deployed  	cafe-1.1.0	1.1.0      	Rollback to 2                                                                                               
    {"name": "chai", "price": "3.10"}
```

</details>

## Self-check

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-6
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "tags v1.0.0 and v1.1.0 (annotated)" '[ "$(git cat-file -t v1.0.0)" = tag ] && [ "$(git cat-file -t v1.1.0)" = tag ]'
check "kind cluster git-course"           'kubectl get nodes --context kind-git-course'
check "the running image is 1.1.0"        'kubectl get deploy cafe -o jsonpath="{.spec.template.spec.containers[0].image}" | grep -qx "cafe:1.1.0"'
check "pods ready"                        'kubectl rollout status deploy/cafe --timeout=60s'
check "Helm history has the rollback"     'helm history cafe | grep -qi "rollback"'
```

```text
ok       tags v1.0.0 and v1.1.0 (annotated)
ok       kind cluster git-course
ok       the running image is 1.1.0
ok       pods ready
ok       Helm history has the rollback
```

## Cleanup

<!-- test: timeout=300 -->
```bash
cd ~ && kind delete cluster --name git-course > /dev/null 2>&1
docker rmi -f cafe:1.0.0 cafe:1.1.0 > /dev/null 2>&1 || true
rm -rf ~/git-practice/project-6 ~/git-practice/deploy-tag.sh ~/git-practice/chart-*
```

Next: [Module 24 · Capstone](../24-capstone/README.md)
