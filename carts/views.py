from django.shortcuts import render
from django.conf import settings
from . models import Cart
from . utils import get_or_create_cart
from . models import Product
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


TEMPLATES = settings.TEMPLATES_DIR
TEMPLATES_APP_CARTS = settings.TEMPLATES_DIR_APP_CART #importing TEMPLATES_APP_PRODUCTS path from Django settings


# Create your views here.
def cart(request):
    template_name = TEMPLATES_APP_CARTS / 'carts' / 'cart.html'

    cart = get_or_create_cart(request)

    context = {
        'cart': cart
    }

    return render (request, template_name, context)

def add(request):
    template_name = TEMPLATES_APP_CARTS / 'carts' / 'add.html'
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.add(product)
    context = { 'product': product }
    return render(request, template_name, context)

def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.remove(product)
    return redirect('carts:cart')

