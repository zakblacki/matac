from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Images_upload,NewsLetterEmails , Comment_images


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full name', 'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'phone number', 'class': 'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}) )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})   )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']
        
        

class UploadImg(forms.Form):
    recu_img = forms.ImageField(required=False,widget=forms.FileInput(attrs={
         
        "id":"id_voucher",
        "accept":"image/*" ,
         
    }))
     
       
from multiupload.fields import MultiFileField
from django.forms.widgets import ClearableFileInput

 
        
 
        
class ImageUploadForm1(forms.Form):
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={
         
        "hidden":"true",
        "id":"comment_image",
        "accept":"image/*" ,
          
    }))
    
    
    
class FormInput(forms.Form):
    recu_img = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        
        'class': 'form-control',
        "hidden":"true",
        "id":"inputFile",
        "accept":"image/*" ,
        "onchange":"readUrl(this)",
         
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
    wilayaship=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':"display:none !important"
    }))
    communship=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':"display:none !important"
    }))
    delivery_type=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':"display:none !important"
    }))
    delivery_price=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':"display:none !important"
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



 
class ImageUploadForm(forms.ModelForm):
    images = MultiFileField(min_num=1, max_file_size=1024*1024*5)
    
    class Meta:
        model = Images_upload
        fields = ('excel_related', 'images')
        
    