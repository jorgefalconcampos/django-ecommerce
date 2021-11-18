from django.urls import path
from . import views

app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAdressesListView.as_view(), name='shipping_addresses')
]