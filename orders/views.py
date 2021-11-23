import threading
from django.shortcuts import redirect
from django.shortcuts import render
from carts.utils import get_or_create_cart
from . models import Order
from . utils import get_or_create_order, breadcrumb
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . utils import destroy_order
from carts.utils import destroy_cart
from orders.utils import destroy_order
from django.shortcuts import get_object_or_404
from . models import Order
from shipping_addresses.models import ShippingAdresses
from . mails import Mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.db.models.query import EmptyQuerySet
from . decorators import validate_cart_and_order


class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()


@login_required(login_url='login')
@validate_cart_and_order
def order (request, cart, order):
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })


@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingadresses_set.count() > 1

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'can_choose_address': can_choose_address,
        'breadcrumb': breadcrumb(address=True)
    })


@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingadresses_set.all()

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })


@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
    shipping_address = get_object_or_404(ShippingAdresses, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')


@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):
    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')
    
    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address
    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_cart(request)
    destroy_order(request)

    messages.success(request, 'Orden cancelada con éxito')

    return redirect('index')


@login_required(login_url='login')
@validate_cart_and_order
def complete(request, cart, order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.complete()

    thread = threading.Thread(target=Mail.send_complete_order, args=(
        order, request.user
    ))

    # Mail.send_complete_order(order, request.user)

    thread.start()

    destroy_cart(request)
    destroy_order(request)

    messages.success(request, 'Orden completada con éxito')

    return redirect('index')
