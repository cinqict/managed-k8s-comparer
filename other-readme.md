# OVH-demo
OVH cloud demo project. Using this demo you will setup an OVH Cloud account and your first project, configure terraform, deploy a managed kubernetes cluster, and deploy nginx.
Since I do not want to deal with your credentials, all setup will happen through the browser and the terminal.
Please remember to use the provided clean-up commands to deprovision all resources.

## Prerequisites
- Terraform
- Kubectl

## Getting started
- Create OVH Cloud account at https://www.ovh.com/auth
- Create project (public cloud -> create new project)
  - Copy the Service_name. (ID under the project name)
- Link your paypal or credit card
- Create credentials for OVH terraform provider [via this link](https://api.ovh.com/createToken/?GET=/*&POST=/*&PUT=/*&DELETE=/*)
  - The terraform provider functions by calling the OVHcloud APIs in the background.

After about a minute payment method will be validated and your project will be created!
Clone this repository and update the values in ovh.conf with your credentials.
If you want, change the tfvars

## Deploying your cluster
Run the following commands:
- ```terraform init```
- ```terraform plan --var-file=terraform.tfvars```
- ```terraform apply --var-file=terraform.tvars --auto-approve```

If you want you can now check your management console to verify that the cluster has been deployed.

## Connecting to your cluster
Now that the cluster has been deployed, we want to connect to it. First get the kube config

### Windows (Powershell)
- ```terraform output -raw kubeconfig | Out-File -FilePath "$HOME\.kube\ovh_cluster.yml" -Encoding utf8```
- ```$env:KUBECONFIG = "$HOME\.kube\ovh_cluster.yml"```

### Unix (I think, please correct if Im wrong)
- ```terraform output -raw kubeconfig > ~/.kube/ovh_cluster.yml```
- ```export KUBECONFIG=~/.kube/ovh_cluster.yml```

Afther switching ```kubectl config get-contexts``` should now return your ovh_cluster context.

## Deploy a demo app
- ```kubectl apply -f deployment.yaml``` to deploy nginx and a load balancer.
- ```kubcetl get svc``` and copy the external IP
- Go to a browser and go to the IP.
- You should now see NGINX!

## Cleaning Up
Remove all your OVH services (Cluster & Load Balancer) by running ```terraform destroy -auto-approve```

### Windows
Reset your kubeconfig by running ```$env:KUBECONFIG = ""```
### Unix (I think)
Reset your kubeconfig by running  ```unset KUBECONFIG```