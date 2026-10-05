# Contributing

1. Start from the latest `main`: `git switch main && git pull`.
2. One branch per change: `git switch -c feat/short-description` (or `fix/…`, `docs/…`, `chore/…`).
3. Commit with Conventional Commits: `feat(menu): add chai`.
4. Run the checks before pushing: `bash scripts/ci.sh`.
5. Push and open a pull request into `main`; describe why, what, and how you tested it.
6. One approval and green checks are required; `main` is protected.
7. Releases: `bash scripts/release.sh X.Y.Z`, then `git push --follow-tags`; the release workflow builds and deploys.

Never commit secrets: configuration with credentials comes from the environment or the secret store.
