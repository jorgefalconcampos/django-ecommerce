from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . models import Product
from django.conf import settings

TEMPLATES = settings.TEMPLATES_DIR_APP_PRODUCTS #importing templates path from Django settings



# Create your views here.
class ProductListView(ListView):

    template_name = TEMPLATES / 'main' / 'index.html'
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductDetailView(DetailView): # id => pk (by default)
    model = Product
    template_name = TEMPLATES / 'products' / 'product.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
