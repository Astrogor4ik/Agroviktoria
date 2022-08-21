import json

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import redirect

from .forms import AddApplicationCustomer
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'pk': product.pk,
                    'name_prod': product.name_prod,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print('Не зареєстрований користувач...')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    last_name = data['form']['last_name']
    phone = data['form']['phone']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email, last_name=last_name, phone=phone,
    )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(pk=item['product']['pk'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order

def AddApplicationUtils(request):
    if request.method == 'POST':
        form = AddApplicationCustomer(request.POST)
        if form.is_valid():

            # print(form.cleaned_data)
            try:
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                Customer.objects.create(name=name, phone=phone)
                messages.success(request, 'Заявка успішно створена, очікуйте на дзвінок від менеджера найближчим часом.')
                return redirect('index')
            except:
                form.add_error(None, 'Ошибка добавления поста')

    else:
        form = AddApplicationCustomer()
    print('form', form)
    return {'form': form}