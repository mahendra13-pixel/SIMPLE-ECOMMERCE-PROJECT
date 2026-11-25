from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db.models import Count,Prefetch
from django.core.paginator import Paginator
from .forms import ReviewForm
from .models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import uuid

# Create your views here.
def index(request):
    offer=OfferProduct.objects.filter(is_available=True)
    category=Category.objects.annotate(sub_count=Count('subcategory')).prefetch_related(Prefetch("subcategory_set",\
    queryset=SubCategory.objects.annotate(product_count=Count("product"))))
    
    subcateid=request.GET.get('subcategory')
    min=request.GET.get('min')
    max=request.GET.get('max')
    if subcateid and min and max:
        product=Product.objects.filter(subcategory=subcateid,price__range=(min,max))
    elif subcateid:
        product=Product.objects.filter(subcategory=subcateid)
    else:

        product=Product.objects.all()

    paginator=Paginator(product,2)
    page=request.GET.get('page')
    data=paginator.get_page(page)
    total=data.paginator.num_pages
    for i in range(total):
        print(i+1)
    context={
        'offer':offer,
        'category':category,
        'product':product,
        'data':data,
        "num":[i+1 for i in range(total)]
    }
    return render(request,'core/index.html',context)


def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    reviews= product.reviews.all()

    form=ReviewForm()
    if request.method == 'POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review =form.save(commit=False)
            review.user=request.user
            review.product=product
            review.save()
            return redirect('product_detail',id=product.id)
    context={
        'product':product,
        'form':form,
        'reviews':reviews,
        'range':range(1,6)
    }
    return render(request,'core/product_detail.html',context)

"""  ===========================add to cart============ """
''' ======================================================='''





@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

import hmac
import hashlib
import base64
#signature

def generate_signature(data, secret):
# signed_field_names must be included in the payload
    signed_fields = data["signed_field_names"].split(",")
# Create message string in exact order
    message = ",".join([f"{field}={data[field]}" for field in signed_fields])
    signature = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode("utf-8")

@login_required(login_url="/users/login")
def cart_detail(request):
    cart=request.session.get('cart')
    amount=0
    for item in cart.values():
        amount+= float(item['price'])*item['quantity']
    amount=round(amount,2)
    tax_amount=round(amount*0.13,2)
    total_amount=round(amount+tax_amount,2)
    transaction_uuid=str(uuid.uuid4())
    product_code='EPAYTEST'
    secret_key='8gBm/:&EnhH.1/q'
    data={
        "amount":amount,
        "tax_amount":tax_amount,
        "total_amount":total_amount,
        "transaction_uuid":transaction_uuid,
        "product_code":product_code,
        "product_service_charge":0,
        "product_delivery_charge":0,
        "success_url":"http://127.0.0.1:8000/payments/success_url",
        "failure_url":"http://127.0.0.1:8000/payments/failure_url",
        "signed_field_names":"total_amount,transaction_uuid,product_code"
    }
    data["signature"]=generate_signature(data,secret_key)
    return render(request, 'core/cart.html',data)