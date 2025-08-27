# Managed Kubernetes Comparer Test Plan

## Overview
This test plan describes how to benchmark and compare managed Kubernetes services across multiple cloud providers (CSPs) using automated pipelines. It covers infrastructure provisioning, application deployment, cluster scaling, load balancer responsiveness, and managed PostgreSQL performance. All results will be collected in JSON format for statistical analysis.

## Pipeline Steps
For each CSP (Azure, OVH, Hetzner, StackIt):
1. **Deploy Infrastructure**
    - Use Terraform to provision the managed Kubernetes cluster, network, and managed PostgreSQL instance.
2. **Deploy Application**
    - Deploy a dummy app (your own dummy-app) to the cluster.
    - Deploy a Kubernetes Service of type LoadBalancer for the app.
3. **Scale-Up Test (Scheduler & Autoscaler Responsiveness)**
    - Increase replicas of dummy app by one per second, until no longer able to schedule
    - Record:
        - Time to trigger scale-up
        - Time until new nodes are ready
        - Time until all pods are scheduled and running
    - Clean up pods after measurement.
    - Note: This approach may not fully simulate real-world application load, but it is effective for triggering autoscaler and measuring cluster responsiveness.
4. **Load Balancer Availability Test**
    - Deploy a Service of type LoadBalancer for the dummy app.
    - Record:
        - Time from Service creation until external IP is assigned (no longer pending)
        - Time until the app is accessible via the external IP
5. **Managed PostgreSQL Performance Test (from within the cluster)**
    - Run a pod with `psql` or a Python script using `psycopg2` to connect to the managed PostgreSQL instance.
    - Measure:
        - Connection latency (ping)
        - Bulk read latency (e.g., SELECT 1000 rows)
        - Bulk write latency (e.g., INSERT 1000 rows)
        - Transaction commit latency
    - Optionally, run these tests multiple times and record all results.
6. **Collect Results**
    - Save all metrics and timestamps in a structured JSON file per run.
    - Upload results as workflow artifacts for later analysis.
    - After 30+ runs per CSP, perform statistical analysis (mean, median, stddev, min, max).

## Metrics to Record
- **Terraform apply duration**
- **External IP availability duration**
- **Scale-up to node ready duration**
- **Node ready to pod scheduled duration**
- **Scale-up to pod scheduled duration**
- **Load balancer provisioning time**
- **PostgreSQL connection latency**
- **PostgreSQL bulk read/write latency**
- **PostgreSQL transaction latency**
- **Any errors or failures during tests**

## Implementation Notes
- Use GitHub Actions to automate the pipeline, looping over all CSPs and running 30+ iterations per provider.
- Store all results as JSON artifacts for each run.
- Use Python or shell scripts for DB tests and result aggregation.
- Use Kubernetes manifests for BusyBox/Nginx scaling and Service creation.
- Clean up resources after each run to avoid quota issues.

## Statistical Analysis
- After all runs, aggregate results and calculate:
    - Mean, median, standard deviation, min, max for each metric
    - Visualize distributions (histograms, boxplots)
    - Compare CSPs on all recorded metrics

---

This test plan ensures a fair, repeatable, and statistically robust comparison of managed Kubernetes services and managed PostgreSQL performance across cloud providers.
