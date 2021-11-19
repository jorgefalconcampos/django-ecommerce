from django.urls import path
from . import views

app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAdressesListView.as_view(), name='shipping_addresses'),
    path('nuevo', views.create, name='create'),
    path('editar/<int:pk>', views.ShippingAdressesUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>', views.ShippingAdressesDeleteView.as_view(), name='delete'),
]