from django.http import HttpResponse, HttpResponseBadRequest
import json
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from hashlib import sha256
from permission import ClassicPermission, AdminPermissions


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
        resp["loggedin"] = True
        resp["phone"] = phone
    else:
        resp = HttpResponseBadRequest("Login failed")
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
    custom_allowed_actions = ['list', 'detail', 'create', 'update']
    allow_all = False


class ItemTypeView(ClassicViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

class Item(ClassicViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class RegistrationUserAgencyView(ClassicViewSet):
    serializer_class = RegistrationSerializer
    allow_all = True
    custom_allowed_actions = ["create"]


class UserView(ClassicViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    custom_allowed_actions = ['retrieve']


class AgencyView(ClassicViewSet):
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()
    custom_allowed_actions = ['retrieve', 'create']


