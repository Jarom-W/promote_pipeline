# GitOps Promotion Pipeline

This repository serves as the GitOps source of truth for Kubernetes deployments and environment promotion workflows.

Rather than allowing CI pipelines to deploy directly to Kubernetes, deployment state is defined and versioned here. ArgoCD continuously reconciles the cluster against the desired state stored in Git, ensuring that infrastructure and application deployments remain declarative, auditable, and reproducible.

The repository is intentionally separated from application source code to enforce a clear boundary between Continuous Integration (CI) and Continuous Delivery (CD).

---

## Architecture Overview

This project implements a production-style GitOps deployment workflow:

```text
Application Repository
        │
        │ Build & Test
        ▼
GitHub Actions
        │
        │ Build Container Image
        ▼
GitHub Container Registry (GHCR)
        │
        │ Open Pull Request
        ▼
GitOps Repository (this repo)
        │
        │ Review / Merge
        ▼
ArgoCD
        │
        │ Reconciliation
        ▼
Kubernetes Cluster
```

CI is responsible for producing immutable deployment artifacts.

CD is responsible for declaring and reconciling desired state.

This separation ensures that deployment decisions are captured in Git history rather than being performed directly by automation against the cluster.

---

## Key Design Principles

### GitOps

All deployment state is defined in Git.

Any change to the cluster must originate from a committed and reviewable change within this repository. ArgoCD continuously compares desired state with live cluster state and automatically reconciles drift.

### Separation of CI and CD

Application repositories build container images and publish them to GHCR using immutable SHA-based tags.

Deployment configuration is maintained separately in this repository, preventing application pipelines from directly mutating cluster state.

### Immutable Deployments

Container images are versioned using Git commit SHAs.

Environment promotion occurs by updating image references rather than rebuilding artifacts, ensuring that the exact same image progresses through the deployment lifecycle.

### Pull Request-Based Promotion

Changes to deployment state are proposed through pull requests, providing:

* Auditability
* Change history
* Review opportunities
* Controlled environment promotion

This mirrors deployment practices commonly used by platform engineering and SRE teams.

---

## Repository Responsibilities

### Helm-Based Application Definitions

Helm charts define reusable Kubernetes resources including:

* Deployments
* Services
* Ingress resources
* Environment-specific configuration

### Environment Configuration

Environment-specific values are maintained independently to support promotion workflows.

```text
environments/
└── http_service/
    ├── dev/
    ├── staging/
    └── prod/
```

Each environment controls deployment characteristics such as:

* Image tag
* Replica count
* Environment-specific settings

### ArgoCD Application Management

ArgoCD Applications are defined and managed from this repository.

A root application follows the App-of-Apps pattern, allowing ArgoCD to discover and manage environment-specific applications declaratively.

---

## Promotion Workflow

1. Application code is merged into the application repository.
2. GitHub Actions builds and publishes a container image tagged with the commit SHA.
3. A pull request is generated against this repository updating the development environment image tag.
4. After review and merge, ArgoCD detects the change and reconciles the cluster.
5. The same image can later be promoted to staging and production through additional GitOps changes without rebuilding artifacts.

This workflow provides a clear and auditable path from source code to production deployment.

---

## Technologies

* Kubernetes
* Helm
* ArgoCD
* GitHub Actions
* GitHub Container Registry (GHCR)
* Docker
* GitOps
* YAML

---

## Goals

This project was built to explore and demonstrate platform engineering concepts including:

* GitOps workflows
* Kubernetes application lifecycle management
* Continuous Delivery architecture
* Environment promotion strategies
* Immutable deployment practices
* Infrastructure as Code
* ArgoCD reconciliation patterns
* Helm-based application packaging

The design intentionally favors production-oriented workflows over convenience-focused automation in order to mirror patterns commonly used by modern platform engineering and SRE teams.
