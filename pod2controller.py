
import yaml
import time
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.client.apis import ApisApi


def load_desired_state(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)

def reconcile(desired_state, observed_state, v1, obj):
    changes = {}
    for key in desired_state:
        # Check if observed_state is None before trying to access it
        if observed_state is None or key not in observed_state or desired_state[key] != observed_state[key]:
            changes[key] = desired_state[key]

    if changes:
        print(f"Applying changes: {changes}")
        try:
            v1.patch_namespaced_custom_object_status(
                group="my.api.group",
                version="v1alpha1",
                namespace=obj['metadata']['namespace'],
                plural="myappresources",
                name=obj['metadata']['name'],
                body={"status": changes}
            )
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->patch_namespaced_custom_object_status: %s\n" % e)


def deploy(k8s_beta):
    try:
        dep = load_desired_state("myappresource.yaml")
        resp = k8s_beta.create_cluster_custom_object(
            group="my.api.group",  
            version="v1alpha1",
            plural="myappresources",
            body=dep)
        print("Deployment created. status='%s'" % str(resp.status))
    except yaml.YAMLError as e:
        print("Failed to load YAML file: ", e)
    except client.rest.ApiException as e:
        print("Failed to create custom object: ", e.reason)
        print("HTTP response headers: ", e.headers)
        print("HTTP response body: ", e.body)
    except Exception as e:
        print("Failed to create custom object: ", e)

def main():
    try:
        config.load_kube_config()
    except Exception as e:
        print("Failed to load kube config: ", e)
        return

v1 = client.CustomObjectsApi()
deploy(v1)
  
    # define desired_state and observed_state
    # 
desired_state = load_desired_state("myappresource.yaml")
observed_state = None
    
reconcile(desired_state, observed_state, v1, obj)
    
    # Add a delay to ensure deployment has been fully created
time.sleep(10)


resource_version = ""
while True:
    stream = watch.Watch().stream(v1.list_cluster_custom_object,
                                  group="my.api.group", version="v1alpha1", plural="myappresources",
                                  resource_version=resource_version
                                  )
    for event in stream:
        obj = event["object"]
        operation = event['type']
        spec = obj.get("spec")

        # Here you should extract the desired state from the spec and the observed state from the status
        desired_state = spec
        observed_state = obj.get("status")

        print(f"Operation: {operation} on myresource: {obj['metadata']['name']}")
        reconcile(desired_state, observed_state, v1, obj)
        resource_version = obj['metadata']['resourceVersion']

            
try:
    config.load_kube_config()
    api_client = client.ApiClient()
except Exception as e:
    print("Failed to load kube config: ", e)

