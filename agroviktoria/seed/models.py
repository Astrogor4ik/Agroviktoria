
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Користувач")
    name = models.CharField(max_length=100, null=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, null=True, verbose_name="Призвіще")
    phone = PhoneNumberField(null=True, blank=False, verbose_name="Номер телефону")
    email = models.EmailField(max_length=100, verbose_name="Емейл")
    # time_create = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    # time_update = models.DateTimeField(auto_now=True, verbose_name="Час останьї зміни")


    def __str__(self):
        return self.name or self.user.username

    class Meta:
        verbose_name = 'Покупець'
        verbose_name_plural = 'Покупець'


class Category(models.Model):
    name_cat = models.CharField(max_length=100, null=True, verbose_name="Категорія")
    slug_cat = models.SlugField(max_length=100, null=True, verbose_name="URL")

    def __str__(self):
        return self.name_cat

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug_cat})

    class Meta:
        verbose_name = 'Види насіння'
        verbose_name_plural = 'Види насіння'


class Product(models.Model):
    name_prod = models.CharField(max_length=100, null=True, verbose_name="Насіння")
    price = models.IntegerField(verbose_name="Ціна")
    content = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Опис")
    slug = models.SlugField(max_length=100, null=True, verbose_name="URL")
    image = models.ImageField()
    image_1 = models.ImageField(blank=True)
    image_2 = models.ImageField(blank=True)
    image_3 = models.ImageField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Час останьї зміни")
    is_published = models.BooleanField(default=True, verbose_name="Публікація")
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name="Категорії")
    digital = models.BooleanField(default=False, null=True, blank=False, verbose_name="Послуга")
    top_sale = models.BooleanField(default=False, null=True, blank=False, verbose_name="Топ продаж")
    landing_rate = models.IntegerField(null=True, verbose_name="Норма висадки(ручна)")
    seeder_landing_rate = models.IntegerField(null=True, verbose_name="Норма висадки(сівалка)")


    def __str__(self):
        return self.name_prod

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})

    class Meta:
        verbose_name = 'Насіння'
        verbose_name_plural = 'Насіння'
        ordering = ['time_create']
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def imageURL_1(self):
        try:
            url = self.image_1.url
        except:
            url = ''
        return url

    @property
    def imageURL_2(self):
        try:
            url = self.image_2.url
        except:
            url = ''
        return url

    @property
    def imageURL_3(self):
        try:
            url = self.image_3.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Деталі замовлення'
        verbose_name_plural = 'Деталі замовлення'
        ordering = ['date_added']
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Покупець")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Замовлення")
    region = models.CharField(max_length=100, null=True, verbose_name="Область")
    city = models.CharField(max_length=100, null=True, verbose_name="Місто")
    mail = models.CharField(max_length=100, null=True, verbose_name="Пошта")
    mail_number = models.CharField(max_length=100, null=True, verbose_name="Номер відділення")
    zipcode = models.CharField(max_length=100, null=True, verbose_name="Поштовий індекс")
    pay = models.CharField(max_length=100, null=True, verbose_name="Оплата")
    comment = models.TextField(max_length=1000, null=True, verbose_name="Коментар")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

