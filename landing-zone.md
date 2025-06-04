# Landing Zone Creation

This section describes the process and components involved in creating a production-ready landing zone for Kubernetes workloads. The landing zone provides the foundational cloud resources and security controls required for deploying and operating applications at scale.

## Core Components

1. **Virtual Network**
   - Provision a virtual network (VNet, VPC, or equivalent) to securely segment and control traffic between resources.
   - Define subnets for the Kubernetes cluster, database, and other services.
   - Configure network security groups/firewall rules for access control.

2. **PostgreSQL Database**
   - Provision a managed PostgreSQL instance for application data storage.
   - Restrict connectivity to trusted sources (e.g., only from the cluster subnet).
   - Enable automated backups and monitoring.

3. **Object Storage**
   - Set up cloud object storage (e.g., Azure Blob Storage, AWS S3, OVH Object Storage) for storing application assets, backups, and logs.
   - Apply bucket policies or access control lists to enforce least-privilege access.

4. **Kubernetes Cluster**
   - Deploy a managed Kubernetes cluster (AKS, EKS, or OVH Managed Kubernetes) in the virtual network.
   - Configure node pools, private networking, network policies, and autoscaling.
   - Enable monitoring and logging integrations.

5. **ArgoCD Installation**
   - Install ArgoCD in the cluster to enable GitOps-based application deployment and management.
   - Secure ArgoCD with RBAC and integrate with your identity provider if possible.

6. **IAM Setup**
   - Define and assign roles for DevOps engineers and application teams using the provider's IAM solution (Entra ID, AWS IAM, OVH IAM).
   - Use groups to manage access to the landing zone resources and Kubernetes RBAC.
   - Store and manage secrets (e.g., database credentials, API keys) securely using the provider's secret management solution or Kubernetes secrets.

## What to Provide DevOps Teams

- Access to the Kubernetes cluster (kubeconfig or federated login)
- Access to ArgoCD (with appropriate RBAC)
- Connection details for PostgreSQL and object storage (as needed)
- Documentation on network boundaries and security controls
- Guidance on using IAM groups/roles for self-service access
- Example CI/CD pipeline templates (e.g., GitHub Actions workflows)

## Automation

All resources should be provisioned using Infrastructure as Code (IaC), preferably with Terraform. This ensures repeatability, version control, and easy collaboration. The Terraform pipeline should:
- Use remote state storage for collaboration and safety.
- Be executed by a dedicated pipeline identity (NPA) with least-privilege permissions.
- Output connection details and credentials as pipeline artifacts or secrets (never in logs).

## Example Workflow

1. Run the Terraform pipeline to provision the landing zone resources.
2. Retrieve outputs (e.g., database connection string, object storage endpoint, kubeconfig).
3. Deploy ArgoCD to the cluster using a Helm chart or manifest.
4. Configure IAM roles/groups for team access.
5. Onboard application teams to deploy workloads via ArgoCD.

This approach ensures a secure, scalable, and developer-friendly foundation for cloud-native workloads.

## Service Connections in GitHub

In Azure DevOps, you create a Service Connection to grant pipelines access to cloud resources. In GitHub, the equivalent is to use GitHub Actions with repository or organization secrets to store credentials (such as cloud provider service principals, API keys, or kubeconfig). For each project team:
- Create a dedicated cloud identity (e.g., Service Principal, IAM user, or API key) with scoped permissions.
- Store the credentials as GitHub Secrets at the repository or organization level.
- Reference these secrets in GitHub Actions workflows to authenticate and deploy resources securely.
- Optionally, use OpenID Connect (OIDC) for federated identity, allowing GitHub Actions to request short-lived credentials from the cloud provider without storing long-lived secrets.
