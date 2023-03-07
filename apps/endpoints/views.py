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

class EnpointViewSet(
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