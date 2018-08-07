from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.db.transaction import atomic
from api.models import *
from hashlib import sha256


class ClassicSerializer(ModelSerializer):
    def save(self, **kwargs):
        self.validated_data["created_by"] = self.context['request'].user
        super(ClassicSerializer, self).save(**kwargs)


class ItemTypeSerializer(ClassicSerializer):
    class Meta:
        model = ItemType
        fields = ('name', )


class ItemSerializer(ClassicSerializer):
    class Meta:
        model = Item
        fields = ('name', 'item_type')


class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = ('name', 'phone', 'is_active', 'created_by')
        read_only_fields = ('is_active', )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone', 'email', 'password_hash', 'is_active')
        write_only_fields = ('password_hash')
        read_only_fields = ()

    def validate_name(self, value):
        return value

    def validate_phone(self, value):
        return value

    def validate_password_hash(self, value):
        return sha256(value).hexdigest()

    def validate_is_active(self, value):
        return value


class RegistrationSerializer(Serializer):
    user_name = serializers.CharField()
    user_password_hash = serializers.CharField()
    user_phone = serializers.CharField()
    user_email = serializers.CharField()
    agency_name = serializers.CharField()
    agency_phone = serializers.CharField()

    @atomic
    def save(self):
        if self.is_valid():
            validated_data = self.validated_data
            user_data = {"name": validated_data["user_name"], "email": validated_data["user_email"], "phone": validated_data["user_phone"], "password_hash": validated_data["user_password_hash"], "is_active": False}
            agency_data = {"name": validated_data["agency_name"], "phone": validated_data["agency_phone"]}

            user = UserSerializer(data=user_data)
            if user.is_valid(raise_exception=True):
                user_validated_data = user.validated_data
                user_obj = User.objects.create(**user_validated_data)

            agency_data["created_by"] = user_obj.id
            agency = AgencySerializer(data=agency_data)
            if agency.is_valid(raise_exception=True):
                agency_obj = Agency.objects.create(**agency.validated_data)
            user_obj.agency = agency_obj
            user_obj.created_by_id = user_obj.id
            user_obj.save()
        else:
            raise ValidationError("validation failed !!")

