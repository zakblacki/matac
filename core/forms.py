from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class FormInput(forms.Form):
    recu_img = forms.ImageField(widget=forms.FileInput(attrs={
        
        'class': 'form-control',
        "hidden":"true",
        "id":"inputFile",
        "accept":"image/*" ,
        "onchange":"readUrl(this)"
    }))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    email =  forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    phone =  forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "pattern":"^(?:0|\(?\+213\)?\s?|00213\s?)[1-79](?:[\.\-\s]?\d\d){4}$"
    }))
    fullname =  forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        
    }))
     

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'

    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
