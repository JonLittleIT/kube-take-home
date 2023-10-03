import kubernetes
from kubernetes.client import ApiClient

# Create ApiClient instance
client = ApiClient()

# Create CustomResourceDefinition object
crd = kubernetes.client.V1CustomResourceDefinition(
    api_version="my.api.group/v1alpha1",
    kind="MyAppResource",
    metadata=kubernetes.client.V1ObjectMeta(name="myappresource.yaml"),
    spec=kubernetes.client.CustomResourceDefinitionSpec(
        group="my.api.group",
        version="v1alpha1",
        scope="Namespaced",
        names=kubernetes.client.CustomResourceDefinitionNames(
            plural="myappresources",
            singular="myappresource",
            kind="MyAppResource",
            listKind="MyAppResourceList"
        )
    )
)

# Create controller to watch for changes
controller = kubernetes.client.BatchV1beta1CronJob(
    api_version="batch/v1beta1",
    kind="CronJob",
    metadata=kubernetes.client.V1ObjectMeta(
        name="myappresource-controller"
    ),
    spec=kubernetes.client.BatchV1beta1CronJobSpec(
        schedule="*/5 * * * *",
        job_template=kubernetes.client.BatchV1beta1JobTemplateSpec(
            spec=kubernetes.client.V1JobSpec(
                template=kubernetes.client.V1PodTemplateSpec(
                    spec=kubernetes.client.V1PodSpec(
                        containers=[
                            kubernetes.client.V1Container(
                                name="myappresource-controller",
                                image="my.api.group/myappresource-controller:v1",
                                command=["python", "controller.py", "--resource=myappresource.yaml"]
                            )
                        ]
                    )
                )
            )
        )
    )
)

# Create the custom resource definition and controller
client.create_custom_resource_definition(crd)
client.create_namespaced_cron_job("default", controller)
