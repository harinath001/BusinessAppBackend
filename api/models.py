from django.db import models
import uuid



class Agency(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey('User', related_name='AGENCY_USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    password_hash = models.TextField()
    email = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', related_name='USER_USER', null=True)
    agency = models.ForeignKey(Agency, null=True, on_delete=models.SET_NULL, related_name='USER_AGENCY')

    def __str__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=32)
    units = models.CharField(max_length=30, default="length")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=256)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid.uuid4()), editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='BOOKING_USER')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='BOOKING_CREATED_BY')

    def __str__(self):
        return self.id


class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid.uuid4()), editable=False)
    vehicle_number = models.CharField(max_length=20)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    driver_phone = models.CharField(max_length=15)
    current_location = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.id


class BookingToDeliveryMapping(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    Delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.booking + " --> " + self.Delivery





