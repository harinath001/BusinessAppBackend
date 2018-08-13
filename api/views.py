from django.http import HttpResponse, HttpResponseBadRequest
import json
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from hashlib import sha256
from permission import ClassicPermission, AdminPermissions, is_user_admin
from backend_filters import OnlyUserFilter, ClassicBackendFilter


def login(request):
    try:
        if "phone" in request.POST:
            phone = request.POST["phone"]
        else:
            phone = request.GET["phone"]
        if "password" in request.POST:
            password = request.POST["password"]
        else:
            password = request.GET["password"]
    except Exception as ex:
        resp = HttpResponseBadRequest("phone number and password required")
        return resp
    password = sha256(password).hexdigest()
    try:
        user = User.objects.get(phone=phone, password_hash=password, is_active=True)
    except Exception as ex:
        print(ex)
        user = None
    if user:
        resp = HttpResponse(json.dumps({"login": "success"}))
        resp["session_action"] = "set_token"
        resp["phone"] = phone
    else:
        resp = HttpResponseBadRequest("Login failed")
        resp["session_action"] = "delete_session"
    return resp


def logout(request):
    if request.user:
        resp = HttpResponseBadRequest("Successfully logged out !!")
        resp["session_action"] = "delete_session"
    else:
        resp = HttpResponseBadRequest("You are not logged in. So logout doesn't matter !!")
        resp["session_action"] = "delete_session"
    return resp

def test(request):
    resp = HttpResponse(json.dumps({"test": "login page"}))
    # resp.set_cookie("test", "test")
    # resp.set_cookie("test2", "test2")
    # print(request.COOKIES)
    # print(str(resp.cookies).split("\n"))
    # print(parse_cookie(str(resp.cookies).split("Set-Cookie:")[1]))
    return resp


class ClassicViewSet(ModelViewSet):
    permission_classes = (ClassicPermission, )
    custom_allowed_methods = ['get', 'post']
    custom_allowed_actions = ['list', 'retrieve', 'create', 'update']
    filter_backends = (OnlyUserFilter, ClassicBackendFilter)
    allow_all = False
    allow_loggedin_users = False
    custom_filters = []
    admin_serializer_class = None

    def get_serializer_class(self):
        if is_user_admin(self.request.user) and self.admin_serializer_class:
            return self.admin_serializer_class
        return self.serializer_class


class ItemTypeView(ClassicViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    filter_backends = (ClassicBackendFilter, )
    custom_allowed_actions = ["retrieve", "list"]
    allow_loggedin_users = True


class ItemView(ClassicViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (ClassicBackendFilter, )
    allow_loggedin_users = True
    custom_allowed_actions = ["list", "retrieve"]


class RegistrationUserAgencyView(ClassicViewSet):
    serializer_class = RegistrationSerializer
    allow_all = True
    custom_allowed_actions = ["create"]


class UserView(ClassicViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    custom_allowed_actions = ['retrieve', 'list']


class UserPasswordUpdateView(ClassicViewSet):
    serializer_class = UserPasswordUpdateSerializer
    queryset = User.objects.all()
    custom_allowed_actions = ["update"]


class UserStatusUpdateView(ClassicViewSet):
    permission_classes = (AdminPermissions, )
    serializer_class = UserStatusSerializer
    queryset = User.objects.all()
    filter_backends = ()
    custom_allowed_actions = ["update"]

    def update(self, request, *args, **kwargs):
        x = super(UserStatusUpdateView, self).update(request, *args, **kwargs)
        # if not request.POST["is_active"]:
        #     print("remove session here")
        return x


class UserLogOut(ClassicViewSet):
    permission_classes = (ClassicPermission, )
    custom_allowed_actions = ["logout"]

    def logout(self, request, *args, **kwargs):
        if hasattr(request.user, "id") and request.user.id:
            resp = HttpResponse("You are successfully logged out of all devices !!")
            resp["session_action"] = "delete_all_sessions"
            resp["user_id"] = request.user.id
        else:
            resp = HttpResponse("You are unidentified. So action cannot be performed!!")
            resp["user_id"] = -1
            resp["session_action"] = "delete_session"
        return resp


class AgencyView(ClassicViewSet):
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()
    custom_allowed_actions = ['retrieve', 'list']
    admin_serializer_class = AgencyAdminSerializer


class DeliveryView(ClassicViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()


class BookingView(ClassicViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


class BookingItemsMappingView(ClassicViewSet):
    serializer_class = BookingItemsMappingSerializer
    queryset = BookingItemsMapping.objects.all()


class BookingToDeliveryMappingView(ClassicViewSet):
    serializer_class = BookingToDeliveryMappingSerializer
    queryset = BookingToDeliveryMapping.objects.all()


class TaxTypeView(ClassicViewSet):
    serializer_class = TaxTypeSerializer
    queryset = TaxType.objects.all()
    custom_allowed_actions = ["retrieve", "list"]
    filter_backends = (ClassicBackendFilter, )


class TaxView(ClassicViewSet):
    serializer_class = TaxSerializer
    queryset = Tax.objects.all()
    filter_backends = (ClassicBackendFilter,)
    custom_allowed_actions = ["retrieve", "list"]


class PaymentView(ClassicViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    custom_allowed_actions = ["retrieve", "list"]


