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
        fields = ('id', 'name', 'units')
        read_only_fields = ('id',)


class ItemSerializer(ClassicSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'item_type')
        read_only_fields = ('id',)


class BookingItemsMappingSerializer(ClassicSerializer):
    class Meta:
        model = BookingItemsMapping
        fields = ('id', 'booking', 'item', 'quantity')
        read_only_fields = ('id',)


class BookingToDeliveryMappingSerializer(ClassicSerializer):
    class Meta:
        model = BookingToDeliveryMapping
        fields = ('id', 'booking', 'delivery')
        read_only_fields = ('id',)


class DeliverySerializer(ClassicSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'vehicle_number', 'date_start', 'date_end', 'driver_phone')
        read_only_fields = ('id',)


class BookingSerializer(ClassicSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'invoice', 'is_active', 'delivery_list', 'payments_list', 'taxes_list', 'items_price_list')
        read_only_fields = ('id', 'delivery_list', 'payments_list', 'taxes_list', 'items_price_list')



class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'name', 'phone', 'created_by', 'is_active')
        read_only_fields = ('is_active', 'id')


class AgencyAdminSerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = ('id', 'name', 'phone', 'created_by', 'is_active')
        read_only_fields = ('id', 'name', 'phone', 'created_by')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone', 'email', 'password_hash', 'is_active')
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }
        read_only_fields = ('id', )

    def validate_name(self, value):
        return value

    def validate_phone(self, value):
        return value

    def validate_password_hash(self, value):
        return sha256(value).hexdigest()

    def validate_is_active(self, value):
        return value


class UserPasswordUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('password_hash', 'id')
        extra_kwargs = {'password_hash': {"write_only":  True}}
        read_only_fields = ('id',)

    def validate_password_hash(self, value):
        return sha256(value).hexdigest()


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone', 'email', 'is_active')
        read_only_fields = ('id',)


class UserStatusSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active', 'id', 'is_admin')
        read_only_fields = ('id',)


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


class TaxTypeSerializer(ClassicSerializer):
    class Meta:
        model = TaxType
        fields = ('id', 'name', )
        read_only_fields = ('id', )


class TaxSerializer(ClassicSerializer):
    class Meta:
        model = Tax
        fields = ('id', 'name', 'tax_type', 'value')
        read_only_fields = ('id', )


class PaymentSerializer(ClassicSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'amount_paid', 'reference_number', 'payment_mode', 'booking')
        read_only_fields = ('id', )
