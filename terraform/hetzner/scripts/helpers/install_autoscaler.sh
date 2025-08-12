#!/bin/bash
# install_autoscaler.sh
# Installs Hetzner Cloud Autoscaler via Helm

set -e

if [ -z "$HCLOUD_TOKEN" ]; then
  echo "Error: HCLOUD_TOKEN environment variable not set."
  exit 1
fi

CLUSTER_NAME="kubernetes-cluster"

helm repo add hcloud https://charts.hetzner.cloud
helm repo update
helm install hcloud-cloud-autoscaler hcloud/hcloud-cloud-autoscaler \
  --namespace kube-system \
  --set hcloud.token=$HCLOUD_TOKEN \
  --set cluster.name=$CLUSTER_NAME
