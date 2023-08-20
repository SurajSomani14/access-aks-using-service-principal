# access-aks-using-service-principal
This Python script uses kubeconfig file from AKS, converts it using kubelogin command line tool for service principal and accesses list of namespaces from AKS.


- Install required packages with the below command

    pip install kubernetes
    
    pip install azure-identity
    
    pip install azure-mgmt-containerservice

- Install Azure CLI. Then install kubelogin with the below command-

      az aks install-cli

- Create a service principal (app registration) in Azure AD. Get client id and client secret.

- Assign below Azure AD role to this app on AKS resource. 

      ***Azure Kubernetes Service Cluster User***
  This role is required in order to read kubeconfig file.

- Set up required Kubernetes RBAC role and role binding.

- Run below Python script to access AKS resources using a service principal
