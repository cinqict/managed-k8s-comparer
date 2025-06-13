# Introduction

## Why Consider European Cloud Providers?

In a cloud landscape dominated by established giants like AWS and Azure, it may seem counterintuitive to explore less mature European cloud providers such as OVH Cloud. However, there are compelling reasons to do so. Data sovereignty, compliance with strict EU regulations (like GDPR), and a desire to reduce dependency on US-based tech companies are driving many organizations to consider European alternatives. Additionally, supporting local providers can foster competition, innovation, and potentially more favorable pricing or support for European customers.

## All well and good, but developers are annoying people
In this world mostly driven by tight budgets and business value, the underlying infrastructure is not the place where you'll improve service or attract customers. We need to keep in mind that we should deliver and maintain a well integrated, stable, secure and practically invisible layer on which all apps will run. In many modern teams this means Managed Kubernetes. In this blog we will discover if OVH is ready to fulfill this role.

## Measuring Developer Experience and Cost

In this blog post, we will compare OVH Cloud, Azure AKS, and AWS EKS by measuring how quickly each provider can deliver a ready-to-use managed Kubernetes cluster. Speed of deployment is crucial: the faster a cluster is provisioned, the sooner developers can start building and deploying applications. We will also examine whether developers can work on an OVH managed cluster without being impacted by performance or feature gaps, and whether OVH offers a cost advantage compared to the more established providers. Our goal is to provide practical insights into whether OVH Cloud is a viable and affordable alternative for production workloads in the European context.

## Setup
To measure:
- Original deployment (Time to Live)
- Installation of argoCD
- App deployment through argoCD - Must write to DB
- Load test
- Node autoscaling delay
- Infra change time and (hopefully no) downtime 
- Cost

> **Note:** SSO and IAM onboarding experience will be covered in detail in a follow-up blog post, as these are critical for team adoption and security but differ significantly between providers.