# this script starts the cluster on microk8s
# it assumes that the cluster is already installed
# and that the user has access to the cluster
# it also assumes that the user has access to the
# docker registry
<<<<<<< HEAD
# create the namespace iotstack
kubectl create namespace iotstack
=======

# start the cluster

## enable the registry
#sudo microk8s enable registry:size=20Gi

## enable the dns
#microk8s enable dns

## enable the dashboard
#microk8s enable dashboard

## enable the storage
#microk8s enable storage

## enable the ingress
#microk8s enable ingress

## enable the metrics server
#microk8s enable metrics-server

## 
#microk8s.kubectl config view --raw > $HOME/.kube/config
>>>>>>> d66a8e21b750c0da362dea48633dfedcac6bce12

## create the namespace iotstack
kubectl create namespace iotstack
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
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
skaffold build

# run skaffold to deploy the application to the namespace iotstack and check for errors 
<<<<<<< HEAD
skaffold dev --namespace iotstack --port-forward --status-check
=======
skaffold dev --namespace iotstack --status-check
>>>>>>> d66a8e21b750c0da362dea48633dfedcac6bce12

# check if the application is running
kubectl get pods --namespace iotstack

<<<<<<< HEAD
# run the following command to get the ip address of tkubectl get ingress --namespace iotstack
=======
# run the following command to get the ip address of the ingress
# microk8s kubectl get ingress --namespace iotstack
>>>>>>> d66a8e21b750c0da362dea48633dfedcac6bce12
