from captcha.fields import CaptchaField
from django.urls import reverse_lazy
from snowpenguin.django.recaptcha3.fields import ReCaptchaField




from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin




class AddApplicationCustomer(SuccessMessageMixin, forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'phone']
        labels = {
            'phone': ('Телефон'), 'name': ("Ім'я")
        }
        error_messages = {
            'phone': {
                'invalid': ("Введіть вірний формат номера телефону(наприклад: +380931234567)!"),
            },
        }


class CreateUserForm(UserCreationForm):
    #captcha = CaptchaField(label='Введіть результат')
    recaptcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



