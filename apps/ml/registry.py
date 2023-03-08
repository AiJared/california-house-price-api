from apps.endpoints.models import Endpoints
from apps.endpoints.models import MLModel
from apps.endpoints.models import MLModelStatus

class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_model(
            self, endpoint_name, model_object, model_name,
            model_status, model_version, owner, model_description,
            model_code
    ):
        # get endpoint
        endpoint, _ = Endpoints.objects.get_or_create(name=endpoint_name, owner=owner)

        # get model
        database_object, model_created = MLModel.objects.get_or_create(
            name=model_name,
            description=model_description,
            code=model_code,
            version=model_version,
            owner=owner,
            parent_endpoint=endpoint
        )

        if model_created:
            status = MLModelStatus(status=model_status,
                                   created_by=owner,
                                   parent_mlmodel=database_object,
                                   active=True)
            status.save()
        # add to registry
        self.endpoints[database_object.id] = model_object