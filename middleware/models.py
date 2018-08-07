from django.db import models
from api.models import User
import uuid


class Sessions(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(primary_key=True, default=str(uuid.uuid4()), editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdminPermissions(models.Model):
    uri_regex = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GeneralPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uri_regex = models.TextField(null=True)
    method = models.CharField(max_length=15, null=True)
    is_allowed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)