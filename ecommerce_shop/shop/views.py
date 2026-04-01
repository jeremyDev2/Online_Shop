from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from cart.forms import CartAddProductForm
from .models import Category, Product
from django.shortcuts import render, get_object_or_404
from .recommender import Recommender

def product_list(request: HttpRequest, category_slug:str|None=None) -> HttpResponse:
    category = None
    categories:QuerySet[Category] = Category.objects.all()
    products:QuerySet[Product] = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category' : category, 'products': products, 'categories':categories})

def product_detail(request:HttpRequest, id, slug:str|None) -> HttpResponse:
    product:Product= get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form:CartAddProductForm = CartAddProductForm()
    r = Recommender()
    recomended_products = r.suggest_the_product([product], 4)
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form':cart_product_form, 'recomended_products': recomended_products})
