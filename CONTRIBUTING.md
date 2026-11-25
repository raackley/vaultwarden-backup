# Contributing

Contributions are welcome! This project is developed on GitHub — please submit
Pull Requests and Issues here.

## Project structure

- `src/` — the backup application (Python)
- `helm/vaultwarden-backup/` — the Helm chart that deploys the backup as a Kubernetes CronJob
- `Dockerfile` — the container image (published to GHCR and Docker Hub)

## Local development

Build the image locally (multi-arch if you have QEMU set up, otherwise drop the flag):

~~~
docker build -t vaultwarden-backup:local .
~~~

Lint the Helm chart:

~~~
helm dependency update helm/vaultwarden-backup/
helm lint helm/vaultwarden-backup/
~~~

## Pull requests

CI runs automatically on every PR and will fail the build if:

- the image fails to build for `linux/amd64` or `linux/arm64`,
- Trivy finds CRITICAL or HIGH severity vulnerabilities in the image, or
- `helm lint` fails.

Non-fork PRs also publish a test image tagged `pr-<PR number>` to
`ghcr.io/raackley/vaultwarden-backup`, which you can pull to try out your
changes in a real cluster:

~~~
docker pull ghcr.io/raackley/vaultwarden-backup:pr-<PR number>
~~~

### If you change the Helm chart

Bump the `version` field in `helm/vaultwarden-backup/Chart.yaml` in the same PR.
Chart versions are published as immutable OCI artifacts, so publishing requires
a new version — a changed chart without a version bump will fail the publish
pipeline after merge.

## Releases

Merging to `master` automatically publishes:

- the image to `ghcr.io/raackley/vaultwarden-backup:latest`, tagged with the commit SHA, and
- the Helm chart to `ghcr.io/raackley/charts/vaultwarden-backup:<chart version>`.

Both are publicly pullable without authentication.