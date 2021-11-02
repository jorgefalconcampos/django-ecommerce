from django.shortcuts import render
from django.conf import settings


TEMPLATES = settings.TEMPLATES_DIR
TEMPLATES_APP_CARTS = settings.TEMPLATES_DIR_APP_CART #importing TEMPLATES_APP_PRODUCTS path from Django settings


# Create your views here.
def cart(request):
    template_name = TEMPLATES_APP_CARTS / 'carts' / 'cart.html'
    print(f"\n\n\n {template_name}" )
    return render (request, template_name)