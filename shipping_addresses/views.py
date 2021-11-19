from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import UpdateView, DeleteView
from . models import ShippingAdresses
from . forms import ShippingAdressesForm
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

class ShippingAdressesListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAdresses
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAdresses.objects.filter(user=self.request.user).order_by('-is_default')



class ShippingAdressesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = ShippingAdresses
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')
    success_message = 'Dirección eliminada'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().is_default:
            return redirect('shipping_addresses:shipping_addresses')
        
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
    
        return super(ShippingAdressesDeleteView, self).dispatch(request, *args, **kwargs)




class ShippingAdressesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = ShippingAdresses
    form_class = ShippingAdressesForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección actualizada con éxito'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)





@login_required(login_url='login')
def create(request):
    form = ShippingAdressesForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False) # when commit=False a shipping address instance is created, but it's not persisted
        shipping_address.user = request.user
        shipping_address.is_default = not ShippingAdresses.objects.filter(user=request.user).exists()

        shipping_address.save() #persisting the instance

        messages.success(request, 'Dirección creada con éxito')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })