# how to instructions


### pre-reqs

### Install the virtualenv package (if using python3)
pip3 install virtualenv

### Navigate to your project directory
cd /path/to/your/project

### Create a new virtual environment
virtualenv venv

### Activate the virtual environment
source venv/bin/activate

## install required packages

pip3 install kubernetes <p>
pip3 install yaml <p>


## install or start minikube (assuming you have brew installed)

brew install minikube

minikube start

## setting up application

Before you can create a Custom Resource, you must first create a Custom Resource Definition (CRD) that defines the new resource type. The CRD defines the resource kind (in this case, `MyAppResource`), and the properties of the resource.

## deploy crd first

```kubectl apply -f crd.yaml```

## create resources from crd and yaml file

```kubectl create -f myappresource.yaml```


## verify its deployed

```kubectl get crd```


![Alt text](image.png)

## verify service is running

```kubectl get crd myappresources.my.api.group -o jsonpath='{.status.conditions[?(@.type == "Established")].status}'```

## verify app is up

```kubectl get pods```

```kubectl describe pod whatever```

## You must port forward so you can access the app on its default port 9898

```kubectl port-forward <pod-name> <host-port>:<pod-port> ```


## if app is running now check in localhost

In a web browser you can access podinfo app at the port forward thats been setup.

```localhost:9898```

### troubleshoot if pod is not started

```

kubectl get myappresources.my.api.group myappresource -n default -o json | jq

```


TRUE - is the response to know its installed and you have e everything setup.


---



![Alt text](image-1.png)


# deploy to cluster with python script

```python3 controller3.py```

```
Script will stay running and update any reconciled differences it needs to make with a patch to the API
This script will deploy a custom object to Kubernetes using the CustomObjectsApi. It will also watch for changes to the custom object and call the reconcile() function to reconcile any differences between the desired state and the observed state. The script will then compare the desired state with the observed state and take the necessary steps to ensure that the observed state matches the desired state. The script also uses the YAML library to parse the information in the myappresource.yaml file and use it to create the custom object. The Kubernetes API client and config library are also used to communicate with the Kubernetes API. Finally, the script will print out information about the operation performed and the name of the custom object.
```
### post use

after done remove resources

```kubectl delete myappresources myappresource```