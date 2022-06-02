from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import CreatUserForm
from .utils import cookieCart,cartData,guestOrder
from django.contrib.auth import authenticate,  login, logout
from django.contrib import messages

# Create your views here.
def store(request):
    data= cartData(request)
    cartItems=data['cartItems']

    products=Product.objects.all()
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'store1/emailsent.html')
        else:

            return redirect('store')
    context={'form':form,'products':products,'cartItems':cartItems}
    return  render(request, 'store1/store.html',context)
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']
        
        
        contact = Contact( name=name,  email=email, subject=subject, phone=phone, message=message)
        contact.save()

        return render(request,'store1/emailsent.html')
    data= cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items= data['items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store1/contact.html',context)
def cart(request):
    data= cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items= data['items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store1/cart.html',context)

def checkout(request):
    data= cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items= data['items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store1/checkout.html',context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('ProductId:', productId)

    customer= request.user.customer
    product=Product.objects.get(id=productId)
    order,created= Order.objects.get_or_create(customer=customer, complete=False)
    
    
    orderItem,created= OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def Login(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')
    data= cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items= data['items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store1/login.html',context)

def Signup(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form= CreatUserForm()
        if request.method == 'POST':
            form = CreatUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
    data= cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items= data['items']
    context={'items':items,'order':order,'cartItems':cartItems,'form':form}
    return render(request, 'store1/signup.html',context)


def logoutUser(request):
	logout(request)
	return redirect('login')