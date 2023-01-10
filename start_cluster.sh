# this script starts the cluster on microk8s
# it assumes that the cluster is already installed
# and that the user has access to the cluster
# it also assumes that the user has access to the
# docker registry

# start the cluster
microk8s start

# enable the registry
sudo microk8s enable registry:size=20Gi

# enable the dns
microk8s enable dns

# enable the dashboard
microk8s enable dashboard

# enable the storage
microk8s enable storage

# enable the ingress
microk8s enable ingress

# enable the metrics server
microk8s enable metrics-server

# 
microk8s.kubectl config view --raw > $HOME/.kube/config

# create the namespace iotstack
microk8s kubectl create namespace iotstack

# check if skaffold is installed and install it if not
if ! command -v skaffold &> /dev/null
then
    echo "skaffold could not be found"
    echo "installing skaffold"
    curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64
    chmod +x skaffold
    sudo mv skaffold /usr/local/bin
fi

# run skaffold to build the application and check for errors
skaffold build --default-repo localhost:32000

# run skaffold to deploy the application to the namespace iotstack and check for errors 
skaffold run --namespace iotstack --default-repo localhost:32000 --port-forward --status-check

# check if the application is running
kubectl get pods --namespace iotstack

# run the following command to get the ip address of the ingress
microk8s kubectl get ingress --namespace iotstack