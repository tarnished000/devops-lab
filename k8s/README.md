# Kubernetes + Argo CD (GitOps)

## Status

Manifests are written and kustomize-valid, but **not yet applied to a real
cluster** — there isn't one yet. The Terraform stage (next in the roadmap)
provisions the cluster on Yandex Cloud; this stage prepares what gets
deployed onto it.

## Structure

- `k8s/base/` — Kustomize base: namespace, Postgres StatefulSet + headless
  Service, app Deployment + Service, Ingress, and an example (unapplied)
  Secret manifest.
- `argocd/application.yaml` — an Argo CD `Application` pointing at this
  repo's `k8s/base`, with automated sync + self-heal.

## Bootstrap (once a cluster exists)

```bash
# 1. Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Create the real DB secret (see k8s/base/secret.example.yaml)
kubectl -n notes-app create namespace notes-app --dry-run=client -o yaml | kubectl apply -f -
kubectl -n notes-app create secret generic notes-db-secret \
  --from-literal=POSTGRES_USER=notes \
  --from-literal=POSTGRES_PASSWORD=<a real generated password> \
  --from-literal=POSTGRES_DB=notes \
  --from-literal=DATABASE_URL=postgresql://notes:<same password>@db:5432/notes

# 3. Point Argo CD at this repo
kubectl apply -f argocd/application.yaml
```

From then on, Argo CD syncs `k8s/base` automatically on every push to `main`.

## Local validation (no cluster needed)

```bash
kubectl kustomize k8s/base
```
