from django.shortcuts import render
from django.conf import settings
from . models import Cart
from . utils import get_or_create_cart

TEMPLATES = settings.TEMPLATES_DIR
TEMPLATES_APP_CARTS = settings.TEMPLATES_DIR_APP_CART #importing TEMPLATES_APP_PRODUCTS path from Django settings


# Create your views here.
def cart(request):
    template_name = TEMPLATES_APP_CARTS / 'carts' / 'cart.html'

    cart = get_or_create_cart(request)

    return render (request, template_name)