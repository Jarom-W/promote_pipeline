# GitOps Promotion Pipeline (CD & Infrastructure)

This repository serves as the single source of truth for the desired state of our Kubernetes infrastructure. Utilizing GitOps principles, it decouples deployment configurations from the application source code to ensure secure, declarative, and auditable infrastructure management.

### Tech Stack & CD Architecture
* **Declarative Manifests:** Uses **Helm** to parameterize Kubernetes resources (Deployments, Services, Ingress) for flexible configuration.
* **GitOps Controller:** **ArgoCD** monitors this repository and continuously reconciles the live cluster state with the definitions stored here.
* **Automated Manifest Updates:** Receives webhooks/repository dispatches from the upstream application repo `sample_http` to automatically update the container image tag in the Helm `values.yaml`.
* **Environment Isolation:** Structured directories or branches separating `dev`, `staging` and `prod` environments to demonstrate a safe promotion path.
