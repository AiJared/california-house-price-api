from rest_framework import serializers
from apps.endpoints.models import Endpoints
from apps.endpoints.models import MLModel
from apps.endpoints.models import MLModelStatus
from apps.endpoints.models import MLRequest

class EnpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoints
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields

class MLModelSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlmodel):
        return MLModelStatus.objects.filter(parent_mlmodel=mlmodel).latest("created_at").status
    
    class Meta:
        model = MLModel
        read_only_fields = ("id", "name", "description", "code", "version", "owner",
                            "created_at", "parent_endpoint", "current_status")
        fields = read_only_fields

class MLModelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "created_by", "created_at",
                  "parent_mlmodel")

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ("id", "input_data", "full_response",
                            "response", "created_at", "parent_mlmodel")
        fields = ("id", "input_data", "full_response", "response", "feedback",
                  "created_at", "parent_mlmodel")
