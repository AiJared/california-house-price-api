import json
import datetime

from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from apps.ml.registry import MLRegistry
from carlifornia.wsgi import registry

from django.shortcuts import render
from django.db import transaction

from rest_framework.exceptions import APIException
from rest_framework import viewsets
from rest_framework import mixins


from apps.endpoints.models import Endpoints
from apps.endpoints.serializers import EnpointSerializer

from apps.endpoints.models import MLModel
from apps.endpoints.serializers import MLModelSerializer

from apps.endpoints.models import MLModelStatus
from apps.endpoints.serializers import MLModelStatusSerializer

from apps.endpoints.models import MLRequest
from apps.endpoints.serializers import MLRequestSerializer

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = EnpointSerializer
    queryset = Endpoints.objects.all()

class MLModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLModelSerializer
    queryset = MLModel.objects.all()

def deactivate_other_statuses(instance):
    old_statuses = MLModelStatus.objects.filter(parent_mlmodel=instance.parent_mlmodel,
                                                created_at__lt=instance.created_at, active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active=False
    MLModelStatus.objects.bulk_update(old_statuses, ["active"])

class MLModelStatusViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = MLModelStatusSerializer
    queryset = MLModelStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))

class MLRequestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        model_status = self.request.query_params.get("status", "production")
        model_version = self.request.query_params.get("version")

        models = MLModel.objects.filter(parent_endpoint__name=endpoint_name, status__status = model_status, status__active=True)

        if model_version is not None:
            models = models.filter(version=model_version)

        if len(models) == 0:
            return Response(
                {"status": "Error", "message": "ML model is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        model_index = 0
        algorithm_object = models[model_index].model
        model_object = algorithm_object['model']
        prediction = model_object.predict(request.data)

        label = prediction[0] if len(prediction) > 0 else "error"
        ml_request =  MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlmodel=models[model_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response({"prediction": label, "request_id": ml_request.id})