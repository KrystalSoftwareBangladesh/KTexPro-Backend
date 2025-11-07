from django.db import models


class Season(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, null=True)
    description = models.TextField(null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
