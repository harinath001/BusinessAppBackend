from django.conf.urls import url
from api.views import *
from django.views.decorators.csrf import csrf_exempt

list_ops = {"get": "list", "post": "create"}
detail_ops = {"get":"retrieve", "post":"update", "put": "update", "delete": "destroy"}
urlpatterns = [
    #Test
    url(regex=r'^testing/?$', view=test),

    #Login
    url(regex=r'^login/?$', view=login),

    #Registration
    url(regex=r'^register/?$', view=RegistrationUserAgencyView.as_view({"post":"create"})),

    #Item type
    url(regex=r'^item_type/(?P<pk>[0-9]+)/?$', view=ItemTypeView.as_view(detail_ops)),
    url(regex=r'^item_type/?$', view=ItemTypeView.as_view(list_ops)),

    #User
    url(regex=r'^user/(?P<pk>[0-9]+)/?$', view=UserView.as_view(detail_ops)),
    url(regex=r'^user/?$', view=UserView.as_view(list_ops)),

    #Agency
    url(regex=r'^agency/(?P<pk>[0-9]+)/$', view=AgencyView.as_view(detail_ops)),
    url(regex=r'^agency/?$', view=AgencyView.as_view(list_ops)),

]
