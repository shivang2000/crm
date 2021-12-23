from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from accounts.decorators import admin_only, allowed_user, unauthenticated_user

from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from .filters import OrderFilter

# Create your views here.
@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else :
            messages.info(request, 'Username or passwords is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):  
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customer': total_customer,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/account_setting.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs 


    context = {
        'customer': customer, 
        'orders': orders,
        'orders_count': orders_count,
        'myFilter':myFilter,
    }
    return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()

    if request.method == "POST":
        print('print POST', request.POST)
        form = OrderForm(request.POST)
        if form.isvalid():
            form.save()
            return redirect('/')


    context = {
        'form': form, 
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    form = OrderForm(instance=Order.objects.get(id=pk))

    if request.method == "POST":
        print('print POST', request.POST)
        form = OrderForm(request.POST, instance=Order.objects.get(id=pk))
        if form.isvalid():
            form.save()
            return redirect('/')
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    if request.method == "POST":
        Order.objects.get(id=pk).delete()
        return redirect('/')

    context = {
        'item': Order.objects.get(id=pk)
    }
    return render(request, 'accounts/delete.html', context)
