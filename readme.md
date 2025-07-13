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
   - Setup Resource Group, Storage Account and a Storage Container for each CSP.
   - Setup App Registration with the following permissions:
     - Storage Blob data contributor on the Storage Account
     - Contributor on the Resource Group
   - Create OVH Cloud account at https://www.ovh.com/auth
   - Create project (public cloud → create new project)

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
    "start": "2025-06-23T13:17:06+00:00",
    "end": "2025-06-23T13:25:20+00:00",
    "duration_seconds": 494
  },
  "external_ip": {
    "start": "2025-06-23T13:29:10.648931+00:00",
    "end": "2025-06-23T13:29:31.389670+00:00",
    "duration_seconds": 20,
    "ip": "20.67.58.192"
  },
  "scaleup": {
    "scaleup_triggered": "2025-06-23T13:32:14+00:00",
    "node_ready": "2025-06-23T13:33:08+00:00",
    "first_pod": "2025-06-23T13:33:08+00:00",
    "node_name": "aks-default-11086619-vmss000001",
    "dur_scaleup_to_ready": 54.0,
    "dur_ready_to_pod": 0.0,
    "dur_scaleup_to_pod": 54.0
  }
}
```

</td>
<td>

```json
{
  "csp": "ovh",
  "terraform_apply": {
    "start": "2025-07-13T19:08:32+00:00",
    "end": "2025-07-13T19:15:14+00:00",
    "duration_seconds": 402
  },
  "external_ip": {
    "start": "2025-07-13T19:16:14.285706+00:00",
    "end": "2025-07-13T19:19:18.992363+00:00",
    "duration_seconds": 184,
    "ip": "37.59.24.5"
  },
  "scaleup": {
    "scaleup_triggered": "2025-07-13T19:22:01+00:00",
    "node_ready": "2025-07-13T19:24:18+00:00",
    "first_pod": "2025-07-13T19:24:16+00:00",
    "node_name": "default-node-c925e7",
    "dur_scaleup_to_ready": 137.0,
    "dur_ready_to_pod": -2.0,
    "dur_scaleup_to_pod": 135.0
  }
}
```

</td>
  </tr>
</table>

---

| Metric                         | Azure | OVH    |
|--------------------------------|-------|--------|
| Terraform apply duration (s)   | 494   | 402    |
| External IP availability (s)   | 20    | 184    |
| Scaleup to ready (s)           | 54.0  | 137.0  |
| Ready to pod (s)               | 0.0   | -2.0   |
| Scaleup to pod (s)             | 54.0  | 135.0  |

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
For this the Workflows `Terraform OVH Destroy` and `Terraform Azure Destroy` are provided.

**NOTE** For some reason the terraform destroy command for OVH can't destroy private networks. Remove it manually if it bothers you.