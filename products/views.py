from django.shortcuts import render
from users.decorators import farmer_required
# Create your views here.
def products(request):
    return render(request,'products/products.html',{})

@farmer_required
def products_add(request):
    return render(request,'products/product_add.html',{})

