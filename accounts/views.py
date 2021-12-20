from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.
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

def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)

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

def deleteOrder(request, pk):
    if request.method == "POST":
        Order.objects.get(id=pk).delete()
        return redirect('/')

    context = {
        'item': Order.objects.get(id=pk)
    }
    return render(request, 'accounts/delete.html', context)
