from django.db import models

class Endpoints(models.Model):
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at =models.DateTimeField(auto_now_add=True,blank=True)

class MLModel(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoints, on_delete=models.CASCADE)

class MLModelStatus(models.Model):
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlmodel = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name="status")

class MLRequest(models.Model):
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlmodel = models.ForeignKey(MLModel, on_delete=models.CASCADE)