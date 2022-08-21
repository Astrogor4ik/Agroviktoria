from captcha.fields import CaptchaField
from snowpenguin.django.recaptcha3.fields import ReCaptchaField



from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class AddApplicationCustomer(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше ім'я")
    phone = PhoneNumberField(label="Номер телефону")
    phone.error_messages['invalid'] = 'Введіть вірний формат номера телефону(наприклад: +380931234567)!'
    captcha = CaptchaField(label='Введіть результат')



class CreateUserForm(UserCreationForm):
    captcha = CaptchaField(label='Введіть результат')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
