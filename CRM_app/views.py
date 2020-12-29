from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from CRM_app.models import *
from CRM_app.forms import OrderForm, CreateUserForm, CustomerForm
from CRM_app.filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request,'Account was Created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request,'CRM_app/register.html',context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request,'Username or Password is Incorrect')
    context = {}
    return render(request,'CRM_app/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['admin','customer'])
def Home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()

    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()

    context= {'customer':customer, 'order':order,
                'total_order':total_order, 'delivered':delivered, 'pending':pending,
             }

    return render(request,'CRM_app/dashboard.html',context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])

@allowed_users(allowed_roles=['admin','customer'])
def userPage(request):
    order = request.user.customer.order_set.all()

    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()

    context = {'order':order,
                'total_order':total_order,
                'delivered':delivered,
                'pending':pending,}
    return render(request,'CRM_app/user.html',context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])

@allowed_users(allowed_roles=['admin','customer'])
def accountSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request,'CRM_app/account_settings.html',context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])

@allowed_users(allowed_roles=['admin','customer'])
def product(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'CRM_app/product.html',context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])

@allowed_users(allowed_roles=['admin','customer'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()

    myFilter = OrderFilter(request.GET,queryset=order)
    order = myFilter.qs

    order_count = order.count()
    context = {'customer':customer, 'order':order, 'order_count':order_count,
                'myFilter':myFilter,}

    return render(request,'CRM_app/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

# @allowed_users(allowed_roles=['admin','customer'])
def order_form(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # formset = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'CRM_app/order_form.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'CRM_app/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'CRM_app/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deletecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context={'customer':customer}
    return render(request,'CRM_app/customer_delete.html',context)
