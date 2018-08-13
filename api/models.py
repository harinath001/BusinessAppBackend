from django.db import models



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
    cost_per_unit = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='BOOKING_USER')
    is_active = models.BooleanField(default=False)
    invoice = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='BOOKING_CREATED_BY')

    def __str__(self):
        return str(self.id)

    @property
    def payment_balance(self):
        return self.total_amount-self.total_payments

    @property
    def total_payments(self):
        a = self.payments_list
        sum = 0.0
        for each in a:
            sum += each["amount_paid"]
        return sum

    @property
    def total_amount(self):
        return self.total_tax+self.items_amount

    @property
    def total_tax(self):
        a = self.taxes_list
        sum = 0.0
        for each in a:
            sum += each["value"]
        return sum

    @property
    def items_amount(self):
        a = self.items_price_list
        sum = 0.0
        for each in a:
            sum += each["price"]
        return sum

    @property
    def items_price_list(self):
        l = []
        try:
            objs = BookingItemsMapping.objects.filter(booking_id=self.id, is_active=True).all()
            for each in objs:
                i = each.item
                o = {}
                o["name"] = i.name
                o["item_type"] = str(i.item_type)
                o["price"] = i.cost_per_unit
                o["quantity"] = each.quantity
                l += [o]
        except Exception as ex:
            print(ex)
        return l

    @property
    def taxes_list(self):
        l = []
        try:
            objs = BookingToTaxMapping.objects.filter(booking_id=self.id, is_active=True).all()
            for each in objs:
                o = {}
                o["name"] = each.name
                o["tax_type"] = str(each.tax_type)
                o["value"] = each.value
                l += [o]
        except Exception as ex:
            pass
        return l

    @property
    def payments_list(self):
        l = []
        try:
            all_objs = Payment.objects.filter(booking_id=self.id, is_active=True).all()
            for each in all_objs:
                o = {}
                o["payment_mode"] = each.payment_mode
                o["amount_paid"] = each.amount_paid
                o["reference_number"] = each.reference_number
                l+=[o]
        except Exception as ex:
            pass
        return l

    @property
    def delivery_list(self):
        l = []
        try:
            all_objs = BookingToDeliveryMapping.objects.filter(booking_id=self.id, is_active=True).all()
            for each in all_objs:
                each = each.delivery
                o = {}
                o["vehicle_number"] = each.vehicle_number
                o["date_start"] = each.date_start
                o["date_end"] = each.date_end
                o["driver_phone"] = each.driver_phone
                o["current_location"] = each.current_location
                l += [o]
        except Exception as ex:
            print(ex)
        return l


class Delivery(models.Model):
    vehicle_number = models.CharField(max_length=20)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    driver_phone = models.CharField(max_length=15, null=True)
    current_location = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return str(self.id)


class Tax(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField()
    tax_type = models.ForeignKey('TaxType')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.name


class TaxType(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return self.name


class BookingToTaxMapping(models.Model):
    booking = models.ForeignKey(Booking)
    tax = models.ForeignKey(Tax)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')


class BookingToDeliveryMapping(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return str(self.booking) + " --> " + str(self.delivery)


class BookingItemsMapping(models.Model):
    booking = models.ForeignKey(Booking)
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')


class Payment(models.Model):
    payment_mode = models.CharField(max_length=30)
    amount_paid = models.FloatField()
    booking = models.ForeignKey('Booking')
    reference_number = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User')

    def __str__(self):
        return str(self.id)





