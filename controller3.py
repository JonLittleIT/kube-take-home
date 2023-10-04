
from kubernetes import client, config, watch
import yaml



def reconcile(desired_state, observed_state):
    # Implement the logic to reconcile differences between desired_state and observed_state
    pass


def deploy():
    try:
        with open("myappresource.yaml") as f:
            dep = yaml.safe_load(f)
            k8s_beta = client.CustomObjectsApi()
            resp = k8s_beta.create_cluster_custom_object(
                group="my.api.group",  # update group
                version="v1alpha1",  # update version
                plural="myappresources",  # update plural to match the kind in lower case and plural form
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
    # Configs can be set in Configuration class directly or using helper utility
    try:
        config.load_kube_config()
    except Exception as e:
        print("Failed to load kube config: ", e)
        return

    deploy()

    v1 = client.CustomObjectsApi()
    resource_version = ""

    while True:
        stream = watch.Watch().stream(v1.list_cluster_custom_object,
                                      group="mygroup", version="v1", plural="myresources",
                                      resource_version=resource_version
                                      )

        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")

            desired_state = spec
            observed_state = obj.get("status")

            print(f"Operation: {operation} on myresource: {obj['metadata']['name']}")
            reconcile(desired_state, observed_state)
            resource_version = obj['metadata']['resourceVersion']


if __name__ == '__main__':
    main()

