from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient
from kubernetes import client, config
import yaml
import json
import os

# make sure your service principal has role assigned on AKS as- Azure Kubernetes Service Cluster User
# this role is required in order to read kubeconfig 

credentials = ClientSecretCredential(
        tenant_id="",       # set your azure tenant id 
        client_id="",       # set client id value
        client_secret=""    # set client secret value
    )
    
    # Instantiate the AKS client
aks_client = ContainerServiceClient(credentials, "<azure subscription id>") # specify azure subscription id

access_profile = aks_client.managed_clusters.list_cluster_user_credentials(
    "<Azure resource group name>", # set azure resource group name where AKS is created
    "<AKS resource name>"  # set name of AKS resource
)

# # Extract the kubeconfig file content from the access profile
kube_config_bytes = access_profile.kubeconfigs[0].value
kube_config_str = kube_config_bytes.decode("utf-8")
kube_config = yaml.safe_load(kube_config_str)

configfile = "customkubeconfig"


with open(configfile, 'w') as file:
    json.dump(kube_config, file)

# Get the current directory path
current_dir = os.getcwd()

# Construct the file path by joining the current directory path and the Filelocation
file_path = os.path.join(current_dir, configfile) 

# currently extracted kubeconfig file from AKS contains local accounts and not service principal that we want to use to access.
# Hence, we need to modify it using kubelogin command line tool. We need to execute convert-kubeconfig command with appropiate parameters.
# to execute, this command from python script, we have used subprocess.
# make sure kubelogin is installed on your machine correctly.
# reference - https://azure.github.io/kubelogin/cli/convert-kubeconfig.html#:~:text=covert%2Dkubeconfig,Exec%20plugin%20will%20be%20converted.

# Define the command
import subprocess
command = [
    "kubelogin",
    "convert-kubeconfig",
    "-l",
    "spn",
    "--client-id",
    "<client id value>",
    "--client-secret",
    "<client secret value>",
    "--kubeconfig",
    file_path
]
# Execute the command
subprocess.run(command, check=True)

# Load converted kubeconfig directly from dictionary
config.load_kube_config(config_file=file_path)
#        config.kube_config.load_kube_config_from_dict(kube_config)

# After loading kubeconfig, we can delete the local file, its optional
if os.path.exists(file_path):
    # Delete the file
    os.remove(file_path)
    print("File deleted successfully.")
else:
    print("File does not exist.")

# Create the API client
k8s_client = client.CoreV1Api()

# Get the list of namespaces for the cluster
namespaces = k8s_client.list_namespace().items  

# Print the list of namespaces
for namespace in namespaces:
    print(namespace.metadata.name)