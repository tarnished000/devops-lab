# devops-lab

Personal learning repo for a Linux/sysadmin → DevOps transition. See
`CLAUDE.md` for the full context (goals, target architecture, how I'm
using it day to day).

The app itself is a small FastAPI + PostgreSQL "notes" CRUD API
(`app/`), deliberately simple — it exists to be the thing the rest of
this repo deploys, monitors and automates, not to be interesting on its
own.

> This GitHub copy mirrors the primary development repo (GitLab). Its
> CI/CD is ported to GitHub Actions + GitHub Container Registry (ghcr.io)
> instead of GitLab CI + GitLab Registry, so the pipeline here runs
> natively on GitHub.

## Status by stage

| Stage | Status |
| --- | --- |
| Docker (app + nginx + Postgres) | Written. Not yet run end-to-end against a live Docker daemon on my side — please `docker compose up -d --build` and sanity-check before trusting it. |
| GitHub Actions CI/CD + Container Registry | Written (`.github/workflows/ci.yml`: pytest against a Postgres service, then build+push to `ghcr.io` using the built-in `GITHUB_TOKEN`, no manual account verification needed). See the Actions tab for the latest run. |
| Ansible | Written (`ansible/`: Docker install, ufw firewall, app deploy roles). Not yet applied — there's no server to target yet; `inventory.ini` is a placeholder until Terraform provisions one. |
| Kubernetes + Argo CD (GitOps) | Written (`k8s/`, `argocd/`). Not yet applied — no cluster exists yet. Kustomize-structured, meant to be picked up by Terraform's output once there's somewhere to run it. |
| Terraform (Yandex Cloud) | Written (`terraform/`). Not yet applied — provisioning needs a real Yandex Cloud account with billing and my own IAM token, which has to happen from outside this environment, by hand. |
| Monitoring (Prometheus/Grafana/Alertmanager) | Wired into `docker-compose.yml` and into the app itself (`/metrics`). Same caveat as Docker: written and internally consistent, not yet watched running live. |

Short version: everything is real, working-quality code, not stubs —
but several stages need something only a human can do (pay for and
provision real cloud infrastructure) before they've actually been *run*,
as opposed to *written*. I'm not going to claim a stage is done just
because the code for it exists.

## Layout

```
app/            FastAPI + SQLAlchemy "notes" API, Dockerfile, tests
nginx/          Reverse proxy config for the app
ansible/        Server configuration (Docker, firewall, app deploy)
k8s/            Kustomize manifests for the app + Postgres
argocd/         Argo CD Application (GitOps sync of k8s/)
terraform/      Yandex Cloud infrastructure (VPC, VM)
monitoring/     Prometheus, Alertmanager, Grafana provisioning
docker-compose.yml            Local stack: app + db + nginx + monitoring
.github/workflows/ci.yml      CI: test, then build + push image to ghcr.io
```

## Running it locally

```bash
cp .env.example .env
docker compose up -d --build
```

- App (via nginx): http://localhost:8080
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Grafana: http://localhost:3000

Each stage's own README (`ansible/README.md`, `k8s/README.md`,
`terraform/README.md`, `monitoring/README.md`) has the details and the
exact commands for that stage.
