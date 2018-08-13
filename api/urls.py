from django.conf.urls import url
from api.views import *
from django.views.decorators.csrf import csrf_exempt

list_ops = {"get": "list", "post": "create"}
detail_ops = {"get":"retrieve", "post":"update", "put": "update", "delete": "destroy"}
urlpatterns = [
    # Test
    url(regex=r'^testing/?$', view=test),

    # Login
    url(regex=r'^login/?$', view=login),

    # Login
    url(regex=r'^logout/?$', view=logout),

    # Registration
    url(regex=r'^register/?$', view=RegistrationUserAgencyView.as_view({"post": "create"})),

    # Item type
    url(regex=r'^item_type/(?P<pk>[0-9]+)/?$', view=ItemTypeView.as_view(detail_ops)),
    url(regex=r'^item_type/?$', view=ItemTypeView.as_view(list_ops)),

    # Item
    url(regex=r'^item/(?P<pk>[0-9]+)/?$', view=ItemView.as_view(detail_ops)),
    url(regex=r'^item/?$', view=ItemView.as_view(list_ops)),

    # User
    url(regex=r'^user/(?P<pk>[0-9]+)/?$', view=UserView.as_view(detail_ops)),
    url(regex=r'^user/?$', view=UserView.as_view(list_ops)),

    # Tax
    url(regex=r'^tax/(?P<pk>[0-9]+)/?$', view=TaxView.as_view(detail_ops)),
    url(regex=r'^tax/?$', view=TaxView.as_view(list_ops)),

    # Tax Type
    url(regex=r'^tax-type/(?P<pk>[0-9]+)/?$', view=TaxTypeView.as_view(detail_ops)),
    url(regex=r'^tax-type/?$', view=TaxTypeView.as_view(list_ops)),

    # User updations
    url(regex=r'^user-password-update/(?P<pk>[0-9]+)/?$', view=UserPasswordUpdateView.as_view(detail_ops)),
    url(regex=r'^user-status-update/(?P<pk>[0-9]+)/?$', view=UserStatusUpdateView.as_view(detail_ops)),
    url(regex=r'^user-logout/(?P<pk>[0-9]+)/?$', view=UserLogOut.as_view({"get": "logout"})),
    url(regex=r'^user-activate/(?P<pk>[0-9]+)/?$', view=UserStatusUpdateView.as_view({"post": "update", "get": "retrieve"})),

    # Agency
    url(regex=r'^agency/(?P<pk>[0-9]+)/?$', view=AgencyView.as_view(detail_ops)),
    url(regex=r'^agency/?$', view=AgencyView.as_view(list_ops)),

    # Delivery
    url(regex=r'^delivery/(?P<pk>[0-9]+)/?$', view=DeliveryView.as_view(detail_ops)),
    url(regex=r'^delivery/?$', view=DeliveryView.as_view(list_ops)),

    # Booking
    url(regex=r'^booking/(?P<pk>[0-9]+)/?$', view=BookingView.as_view(detail_ops)),
    url(regex=r'^booking/?$', view=BookingView.as_view(list_ops)),

    # BookingToItem
    url(regex=r'^booking-to-items/(?P<pk>[0-9]+)/?$', view=BookingItemsMappingView.as_view(detail_ops)),
    url(regex=r'^booking-to-items/?$', view=BookingItemsMappingView.as_view(list_ops)),
    url(regex=r'^booking-to-items/booking-id/(?P<pk>[0-9]+)/?$', view=BookingItemsMappingView.as_view({"get": "all_items_in_booking"})),

    # BookingToDelivery
    url(regex=r'^booking-to-delivery/(?P<pk>[0-9]+)/?$', view=BookingToDeliveryMappingView.as_view(detail_ops)),
    url(regex=r'^booking-to-delivery/?$', view=BookingToDeliveryMappingView.as_view(list_ops)),

]