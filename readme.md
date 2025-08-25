# Managed Kubernetes Comparer

This repository is used to compare the performance of managed Kubernetes services from different Cloud Service Providers (CSPs), currently implemented are Azure and OVHcloud. It automates the deployment of a dummy application, runs benchmarks, and collects results for analysis.

Hetzner setup implementation based on the [tutorial by Alexdru Popescu](https://community.hetzner.com/tutorials/setup-your-own-scalable-kubernetes-cluster)

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
   - Setup Resource Group, Storage Account and a Storage Container for each CSP.
   - Setup App Registration with the following permissions:
     - Storage Blob data contributor on the Storage Account
     - Contributor on the Resource Group
   - If using OVH
    - Create OVH Cloud account at https://www.ovh.com/auth
    - Create project (public cloud → create new project)
   - If using Hetzner
    - Create Hetzner account at https://accounts.hetzner.com/signUp
    - Create project
    - Create API token (project → security → API tokens)
   - If using Stackit
    - Create Stackit account (requires an invite, ask Bouke)
    - Create a project in the CINQ Organization at https://portal.stackit.cloud/organization/68e8593b-2b3c-4c6f-8a72-dfb81f47926e
    - Create a service account (IAM → Service Accounts → Create)

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
| `HETZNER_API_TOKEN`      | Read & Write token for Hetzner Terraform    | Yes         | [Hetzner Console](https://console.hetzner.com) → Security → API Tokens       |
| `STACKIT_SERVICE_ACCOUNT_KEY`     | Service Account Credentials for Stackit     | Yes         | [Stackit Portal](https://portal.stackit.cloud/service-accounts/wizard?project=cdae8eed-9d4f-49d4-a059-9fe987c52735) → Service Accounts       |
| `STACKIT_PROJECT_ID`     | Project ID for Terraform Deployment         | Yes         | [Stackit Portal](https://portal.stackit.cloud/organization/68e8593b-2b3c-4c6f-8a72-dfb81f47926e) → Select Project → Create Resource       |

### Required Variables

| Secret Name           | Description                                 | Required    | Where to Get It                                           |
|-----------------------|---------------------------------------------|-------------|-----------------------------------------------------------|
| `RESOURCE_GROUP_NAME` | Existing RG name for TF backend             | Yes         | Azure Portal → Resource Groups                            |
| `STORAGE_ACCOUNT_NAME`| Existing SA name for TF backend             | Yes         | Azure Portal → Resource Groups → Storage Account          |
| `AZ_SUBSCRIPTION_ID`  | Azure Subscription ID                       | Yes         | Azure Portal → Subscriptions                              |
| `AZ_TENANT_ID`        | Azure Tenant ID                             | Yes         | Azure Portal → Azure Entra ID                             |
| `OVH_ENDPOINT`        | OVH API endpoint (e.g., ovh-eu)             | Yes         | [OVH API Docs](https://docs.ovh.com/gb/en/api/)           |

## Demo mode
A demo mode is included which can be used by selecting the checkbox on the workflow during a manual run. This mode skips the automatic load test and install grafana on your cluster.
You can access it by following these steps:
 1. Download Kubeconfig artifact from the workflow
 2. Connect to the cluster
 3. Run `kubectl port-forward svc/grafana -n monitoring 3000:80`
 4. Open a browser and go to http://localhost:3000
 5. Log in using admin admin
 6. Click on the `+` on the top right and import dashboard
 7. Import 315 or 1860

## Results

I ran it once for both CSPs (OVH & Azure) and got the following results:

<table>
  <tr>
    <td>

```json
{
  "csp": "azure",
  "terraform_apply": {
    "tf_start": "2025-08-24T09:50:34+00:00",
    "tf_end": "2025-08-24T09:56:47+00:00",
    "tf_duration_seconds": 373,
    "post_apply_end": "2025-08-24T09:56:47+00:00",
    "post_apply_duration_seconds": 0,
    "total_duration_seconds": 373
  },
  "external_ip": {
    "start": "2025-08-24T09:58:49.044349+00:00",
    "end": "2025-08-24T09:59:09.802208+00:00",
    "duration_seconds": 20,
    "ip": "132.220.38.91"
  },
  "scaleup": {
    "scaleup_triggered": "2025-08-24T10:01:28+00:00",
    "node_ready": "2025-08-24T10:02:50+00:00",
    "first_pod": "2025-08-24T10:02:35+00:00",
    "node_name": "aks-default-26398082-vmss000001",
    "dur_scaleup_to_ready": 82.0,
    "dur_ready_to_pod": -15.0,
    "dur_scaleup_to_pod": 67.0
  }
}
```

</td>
<td>

```json
{
  "csp": "ovh",
  "terraform_apply": {
    "tf_start": "2025-08-24T14:13:48+00:00",
    "tf_end": "2025-08-24T14:20:58+00:00",
    "tf_duration_seconds": 430,
    "post_apply_end": "2025-08-24T14:20:58+00:00",
    "post_apply_duration_seconds": 0,
    "total_duration_seconds": 430
  },
  "external_ip": {
    "start": "2025-08-24T14:21:54.544977+00:00",
    "end": "2025-08-24T14:24:30.827427+00:00",
    "duration_seconds": 156,
    "ip": "51.178.114.67"
  },
  "scaleup": {
    "scaleup_triggered": "2025-08-24T14:26:58+00:00",
    "node_ready": "2025-08-24T14:29:31+00:00",
    "first_pod": "2025-08-24T14:29:27+00:00",
    "node_name": "default-node-804fb0",
    "dur_scaleup_to_ready": 153.0,
    "dur_ready_to_pod": -4.0,
    "dur_scaleup_to_pod": 149.0
  }
}
```

</td>
  </tr>
  <tr>
<td>

```json
{
  "csp": "hetzner",
  "terraform_apply": {
    "tf_start": "2025-08-24T09:02:44+00:00",
    "tf_end": "2025-08-24T09:03:35+00:00",
    "tf_duration_seconds": 51,
    "post_apply_end": "2025-08-24T09:04:39+00:00",
    "post_apply_duration_seconds": 64,
    "total_duration_seconds": 115
  },
  "external_ip": {
    "start": "2025-08-24T09:05:16.060347+00:00",
    "end": "2025-08-24T09:05:43.328797+00:00",
    "duration_seconds": 27,
    "ip": "91.98.15.226"
  },
  "scaleup": {
    "scaleup_triggered": "2025-08-24T09:06:57+00:00",
    "node_ready": "2025-08-24T09:07:25+00:00",
    "first_pod": "2025-08-24T09:07:25+00:00",
    "node_name": "pool1-1a722db4343937e4",
    "dur_scaleup_to_ready": 28.0,
    "dur_ready_to_pod": 0.0,
    "dur_scaleup_to_pod": 28.0
  }
}
```
</td>
<td>

```json
{}
```
</td>
  </tr>
</table>

---

| Metric                         | Azure | OVH    | Hetzner | StackIt |
|--------------------------------|-------|--------|---------|---------|
| Terraform apply duration (s)   | 373   | 430    | 115     |         |
| External IP availability (s)   | 20    | 156    | 27      |         |
| Scaleup to ready (s)           | 82.0  | 153.0  | 28.0    |         |
| Ready to pod (s)               | -15.0 | -4.0   | 0.0     |         |
| Scaleup to pod (s)             | 67.0  | 149.0  | 28.0    |         |

### Metrics Explained

- **Terraform apply duration (s):**  
  The total time it took for Terraform to provision the Kubernetes cluster and all required infrastructure resources on the cloud provider.

- **External IP availability (s):**  
  The time from the end of infrastructure provisioning until the dummy application received a public (external) IP address and became accessible from the internet.

- **Scaleup to ready (s):**  
  The time between triggering a node scale-up (e.g., due to increased load or a manual request) and the new node reporting as "Ready" in the Kubernetes cluster.

- **Ready to pod (s):**  
  The time from when the new node is "Ready" until the first pod is successfully scheduled and running on that node.

- **Scaleup to pod (s):**  
  The total time from triggering the scale-up until the first pod is running on the new node. This is the sum of "Scaleup to ready" and "Ready to pod".

These metrics help compare the responsiveness and provisioning speed of managed Kubernetes services across different CSPs

## Cleaning Up
Don't forget to remove your provisioned resources once you are done.
For this the Workflow `Terraform Destroy` is provided.

**NOTE** For some reason the terraform destroy command for OVH can't destroy private networks. Remove it manually if it bothers you.