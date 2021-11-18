from django.shortcuts import render
from django.views.generic import ListView
from . models import ShippingAdresses
from . forms import ShippingAdressesForm

# Create your views here.


class ShippingAdressesListView(ListView):
    model = ShippingAdresses
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAdresses.objects.filter(user=self.request.user).order_by('-is_default')



def create(request):
    form = ShippingAdressesForm()
    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })