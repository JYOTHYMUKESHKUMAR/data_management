from django.shortcuts import render,HttpResponse,get_object_or_404
from django.shortcuts import render
from .models import UpdateCashIn, UpdateCashOut
from .models import *

# Create your views here.
##def index(request):
    #return HttpResponse("Hello")


def allProdcat(request, c_slug=None):
    c_page = None
    products = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        products = Product.objects.filter(available=True)

    context = {
        'category': c_page,
        'products': products,
    }

    return render(request, 'category.html', context)

def Product_Detail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

