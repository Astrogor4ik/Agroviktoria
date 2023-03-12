from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
import json
import datetime
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import CreateUserForm, AddApplicationCustomer
from .models import *
from .utils import cookieCart, cartData, guestOrder #AddApplicationUtils
from django.contrib.messages.views import SuccessMessageMixin

menu = [{'title': "Головна сторінка", 'url_name': 'index'},
        {'title': "Купити насіння", 'url_name': 'store'},
        {'title': "Послуга очистки насіння", 'url_name': 'clean_seed'},
        {'title': "Про нас", 'url_name': 'about'},
        {'title': "Місцезнаходження", 'url_name': 'we_on_map'},
        {'title': "Доставка та оплата", 'url_name': 'delivery'},
        {'title': "Контакти", 'url_name': 'contact'}
]


class AgroHome(ListView):
    model = Product
    template_name = 'seed/index.html'
    context_object_name = 'products'
    #extra_context = {'title': 'Головна сторінка'}


    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        data = cartData(self.request)
        contex['cartItems'] = data['cartItems']
        contex['menu'] = menu
        return contex


    def get_queryset(self):
        return Product.objects.filter(is_published = True)



def main(request):

    context = {}
    return render(request, 'seed/main.html', context)

class Store(ListView):
    paginate_by = 6
    model = Product
    template_name = 'seed/store.html'
    context_object_name = 'products'
    products = Product.objects.all().select_related('cat')
    categories = Category.objects.all()

    def get_queryset(self):
        serch_query = self.request.GET.get('search', '')
        products_2 = Product.objects.filter(Q(name_prod__icontains=serch_query) | Q(content__icontains=serch_query)).select_related('cat')
        return products_2


    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        data = cartData(self.request)
        contex['cartItems'] = data['cartItems']
        contex['menu'] = menu
        contex['products_2'] = self.get_queryset
        contex['cat_selected'] = 0
        contex['categories'] = self.categories
        contex['products'] = self.products

        return contex


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items,
               'order': order,
               'cartItems': cartItems,
               'menu': menu,
               }
    return render(request, 'seed/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items,
               'order': order,
               'cartItems': cartItems,
               'menu': menu,
               }
    return render(request, 'seed/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "add2":
        orderItem.quantity = (orderItem.quantity + 10)
    elif action == "add3":
        orderItem.quantity = (orderItem.quantity + 100)
    elif action == "add4":
        orderItem.quantity = (orderItem.quantity + 5)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == "remove2":
        orderItem.quantity = (orderItem.quantity - 10)
    elif action == "remove3":
        orderItem.quantity = (orderItem.quantity - 100)
    elif action == "remove4":
        orderItem.quantity = (orderItem.quantity - 5)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def multi(a,b):
    if a and b:
        return a * b or print(f'These {a} and {b} aren`t numbers!')


def show_post(request, prod_slug):
    pub = get_object_or_404(Product, slug=prod_slug)
    data = cartData(request)
    cartItems = data['cartItems']
    categories = Category.objects.all()
    products = Product.objects.all().select_related('cat')
    if request.method == 'POST':
        try:
            acre_val = int(request.POST.get('acre_val', False))
            rate_val = int(request.POST.get('rate_val', False))
            res = multi(acre_val, rate_val)
        except:
            return redirect('store')
    else:
        res = 0
    context = {'pub': pub,
               'products': products,
               'categories': categories,
               'menu': menu,
               'cartItems': cartItems,
               'cat_selected': 0,
               "res": res

               }
    return render(request, 'seed/product.html', context)


def show_category(request, cat_slug):
    products_2 = Product.objects.filter(cat__slug_cat=cat_slug).select_related('cat')
    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    if len(products_2) == 0:
        raise Http404()

    paginator = Paginator(products_2, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = Product.objects.all().select_related('cat')


    context = {
        'products': products,
        'products_2': products_2,
        'categories': categories,
        'menu': menu,
        'cartItems': cartItems,
        'cat_selected': cat_slug,
        'page_obj': page_obj,

    }

    return render(request, 'seed/store.html', context=context)

class CleanSeed(SuccessMessageMixin, CreateView):
    form_class = AddApplicationCustomer
    template_name = 'seed/clean_seed.html'
    success_url = reverse_lazy('index')
    success_message = "Заявка успішно створена, очікуйте на дзвінок від менеджера найближчим часом."



    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        data = cartData(self.request)
        contex['cartItems'] = data['cartItems']
        contex['menu'] = menu
        return contex



def about(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'menu': menu,
               'cartItems': cartItems
               }
    return render(request, 'seed/about.html', context)


def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'menu': menu,
               'cartItems': cartItems
               }

    return render(request, 'seed/contact.html', context)


def delivery(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'menu': menu,
               'cartItems': cartItems
               }

    return render(request, 'seed/delivery.html', context)


def we_on_map(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'menu': menu,
               'cartItems': cartItems,
               }
    return render(request, 'seed/we_on_map.html', context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    cookieData = cookieCart(request)
    items = cookieData['items']

    if request.user.is_authenticated:
        name = data['form']['name']
        last_name = data['form']['last_name']
        phone = data['form']['phone']
        email = data['form']['email']
        customer = Customer.objects.get(user=request.user)
        customer.name = name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.save()
        #order = Order.objects.filter(customer=customer, complete=False).first()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.date_orderd = datetime.datetime.now()
        order.save()
        for item in items:
            product = Product.objects.get(pk=item['product']['pk'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )


    else:
        customer, order = guestOrder(request, data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            region=data['shipping']['region'],
            city=data['shipping']['city'],
            mail=data['shipping']['mail'],
            mail_number=data['shipping']['mail_number'],
            zipcode=data['shipping']['zipcode'],
            pay=data['shipping']['pay'],
            comment=data['shipping']['comment'],
        )
    return JsonResponse('Payment complete!', safe=False)

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            Customer.objects.create(user=user)

            user = form.cleaned_data.get('username')
            messages.success(request, f'Аккаун для {user} створений. Увійдіть в аккаунт.')
            return redirect('login')


    context = {'form': form,
               'menu': menu,
               'cartItems': 0,
               }
    return render(request, 'seed/register.html', context)


def login_user(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = User.objects.get(email=email.lower()).username

            user = authenticate(request, username=username, password=password)
            # user_p = authenticate(request, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, "Некоректний емейл або пароль.")
                return redirect('login')
        except:
            messages.info(request, "Некоректний емейл або пароль.")
            return redirect('login')


    context = {'menu': menu,
               'cartItems': 0,}
    return render(request, 'seed/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')





