from django import forms
from .models import PaymentType

# Choice_PaymentTypes = ((1,"پرداخت از طریق درگاه بانکی"),(2,"پرداخت در محل"))
class OrderForm(forms.Form):
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
                           error_messages={'required':'این فیلد نمی تواند خالی باشد'})
    family = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
                           error_messages={'required':'این فیلد نمی تواند خالی باشد'})
    email = forms.CharField(label="",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
                             required=False)
    phone_number = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
                             required=False)
    address = forms.CharField(label="",
                             widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس'}),
                             error_messages={'required': 'این فیلد نمی تواند خالی باشد'})
    description = forms.CharField(label="",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس'}),
                              required=False)
    payment_type = forms.ChoiceField(label="",
                                     choices=[(item.pk,item) for item in PaymentType.objects.all()],
                                     widget=forms.RadioSelect(),)