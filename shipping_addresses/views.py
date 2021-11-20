from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from . models import ShippingAdresses
from . forms import ShippingAdressesForm
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order

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

        return super(ShippingAdressesUpdateView, self).dispatch(request, *args, **kwargs)





@login_required(login_url='login')
def create(request):
    form = ShippingAdressesForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False) # when commit=False a shipping address instance is created, but it's not persisted
        shipping_address.user = request.user
        shipping_address.is_default = not request.user.has_shipping_address()

        shipping_address.save() #persisting the instance

        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Dirección creada con éxito')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })


@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAdresses, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')