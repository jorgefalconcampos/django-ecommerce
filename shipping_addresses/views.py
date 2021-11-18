from django.shortcuts import render
from django.views.generic import ListView
from . models import ShippingAdresses
# Create your views here.


class ShippingAdressesListView(ListView):
    model = ShippingAdresses
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAdresses.objects.filter(user=self.request.user).order_by('-is_default')

