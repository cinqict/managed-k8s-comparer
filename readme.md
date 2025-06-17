Blog Post Outline:

Introduction: Purpose, what is a “production ready” managed Kubernetes cluster, and why compare OVH Cloud, Azure AKS, and AWS EKS.
Prerequisites: What you need (accounts, CLI tools, permissions).
Terraform Remote State Management:
- Why remote state is important (collaboration, safety, automation).
- How to configure remote state for each provider:
  - Azure: Storage Account backend example.
  - AWS: S3 + DynamoDB backend example.
  - OVH: S3-compatible Object Storage backend example.
- Storing backend credentials securely in Azure DevOps and GitHub Actions (using secrets/variables).
- Example backend blocks for each provider.
Cluster Creation:
Step-by-step for each provider (OVH, Azure, AWS).
Note any differences in setup, configuration, and available options.
Deployment Time Comparison:
Measure and record the time from cluster creation command to ready state.
Cost Comparison:
Compare pricing for similar node types and configurations.
Feature Comparison:
Networking, autoscaling, security, monitoring, integrations, etc.
RBAC & Access Management for Collaboration:
- Azure: Using Entra ID groups to provide RBAC access to landing zones for DevOps engineers.
- AWS: Using IAM groups/roles and SSO for RBAC access to AWS web console and resources.
- OVH: Using OVH IAM (Identity & Access Management) to assign roles/groups for RBAC access.
- Best practices for enabling team collaboration securely.
Pipeline Identity & Permissions (NPA for Terraform):
- Azure: Using App Registration (Service Principal) for Terraform pipeline identity.
- AWS: Using IAM user/role with programmatic access for Terraform pipeline.
- OVH: Using API credentials (application keys) for Terraform pipeline.
- Security considerations and least privilege principle.
Does OVH Cloud offer all the features you expect?
Conclusion: Summary, recommendations, and your experience.
Practical Steps:

Prepare scripts or CLI commands for creating clusters on each platform (using PowerShell, Azure CLI, AWS CLI, and OVH CLI/API).
Define what “production ready” means for you (e.g., private networking, autoscaling, monitoring, RBAC, etc.).
Time each deployment (use PowerShell’s Measure-Command or similar).
Gather pricing info from each provider’s calculator for the same configuration.
Document any missing features or differences.
Would you like example scripts for cluster creation on each platform, or help with structuring the blog post in more detail?

kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl port-forward svc/grafana -n argocd 3000:443