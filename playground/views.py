from django.shortcuts import render
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def say_hello(request):

    product = Product.objects.filter(title__icontains="rice")
    return render(request,"index.html", {"name": "Kipruto Victor", "products":list(product)})
