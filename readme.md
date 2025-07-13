# Managed Kubernetes Comparer

This repository is used to compare the performance of managed Kubernetes services from different Cloud Service Providers (CSPs), currently implemented are Azure and OVHcloud. It automates the deployment of a dummy application, runs benchmarks, and collects results for analysis.

## Usage

1. **Configure Secrets:**  
   Before running the workflows, ensure all required secrets are set in your repository or organization settings (GitHub → Settings → Secrets and variables → Actions).

2. **Run the CI/CD Pipeline:**  
   The K8s Benchmark Master Flow GitHub Actions workflow will:
   - Provision a Kubernetes cluster
   - Build and push a Docker image (if credentials are provided)
   - Deploy the dummy app to the target Kubernetes cluster
   - Run benchmarks and collect results

3. **Analyze Results:**  
   Benchmark results will be available as workflow artifacts for download and comparison.

## Prerequisites
   - Setup Resource Group, Storage Account & Storage Container.
   - Setup App Registration with the following permissions:
     - Storage Blob data contributor on the Storage Account
     - Contributor on the Resource Group
   - Create OVH Cloud account at https://www.ovh.com/auth
   - Create project (public cloud -> create new project)

### Required Secrets

| Secret Name              | Description                                 | Required    | Where to Get It                                           |
|--------------------------|---------------------------------------------|-------------|-----------------------------------------------------------|
| `DOCKERHUB_USERNAME`     | Docker Hub username                         | No          | [Docker Hub Account Settings](https://hub.docker.com/)    |
| `DOCKERHUB_TOKEN`        | Docker Hub access token/password            | No          | [Docker Hub Security Settings](https://hub.docker.com/)   |
| `AZ_CLIENT_ID`           | Azure Service Principal Client ID           | Yes         | Azure Portal → Azure AD → App registrations               |
| `AZ_CLIENT_SECRET`       | Azure Service Principal Client Secret       | Yes         | Azure Portal → Azure AD → App registrations               |
| `OVH_APPLICATION_KEY`    | OVH API application key                     | Yes         | [OVH API Credentials](https://www.ovh.com/auth/api/createToken?GET=/*&POST=/*&PUT=/*&DELETE=/*)     |
| `OVH_APPLICATION_SECRET` | OVH API application key                     | Yes         | [OVH API Credentials](https://www.ovh.com/auth/api/createToken?GET=/*&POST=/*&PUT=/*&DELETE=/*)     |
| `OVH_CONSUMER_KEY`       | OVH API consumer key                        | Yes         | [OVH API Credentials](https://www.ovh.com/auth/api/createToken?GET=/*&POST=/*&PUT=/*&DELETE=/*)     |
| `OVH_PROJECT_ID`         | OVH Public Cloud project ID                 | Yes         | OVHcloud Control Panel → Public Cloud → Project Info      |

### Required Variables

| Secret Name           | Description                                 | Required    | Where to Get It                                           |
|-----------------------|---------------------------------------------|-------------|-----------------------------------------------------------|
| `RESOURCE_GROUP_NAME` | Existing RG name for TF backend             | Yes         | Azure Portal → Resource Groups                            |
| `STORAGE_ACCOUNT_NAME`| Existing SA name for TF backend             | Yes         | Azure Portal → Resource Groups → Storage Account          |
| `AZ_SUBSCRIPTION_ID`  | Azure Subscription ID                       | Yes         | Azure Portal → Subscriptions                              |
| `AZ_TENANT_ID`        | Azure Tenant ID                             | Yes         | Azure Portal → Azure Entra ID                             |
| `OVH_ENDPOINT`        | OVH API endpoint (e.g., ovh-eu)             | Yes         | [OVH API Docs](https://docs.ovh.com/gb/en/api/)           |