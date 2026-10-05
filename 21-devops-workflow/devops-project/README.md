# Cafe: a DevOps repository

The cafe menu website, packaged as a container image and deployed to Kubernetes with Helm.

```text
devops-project/
├── application/          the website (static files: index.html, menu.json)
├── Dockerfile            the container image (nginx, non-root)
├── VERSION               the release version, the single source of truth
├── helm/cafe/            the Helm chart (appVersion and image tag follow VERSION)
├── kubernetes/           cluster-level manifests (namespace)
├── scripts/              ci.sh (checks), release.sh (version + tag), deploy.sh (deployment)
├── docs/                 CONTRIBUTING.md: the team's Git workflow
└── .github/workflows/    ci.yml (every PR and main), release.yml (tags v*: image to GHCR, GitHub release)
```

Quick start: `bash scripts/ci.sh`. Workflow: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
