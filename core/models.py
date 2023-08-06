from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from multiupload.fields import MultiImageField
import datetime
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)

LABEL_CHOICES_GENDER=(
    ('M', 'MALE'),
    ('F', 'FEMALE'),
    ('M-F', 'MALE-FEMALE'),
    ('E', 'ENFANTS')
)


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)



class Essential(models.Model):
    model_type=models.CharField(max_length=150)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    price= models.IntegerField()
    button_text= models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.line1, self.price)





class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,max_length=190)
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
     

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

class ExcelFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='excel_files/')


class ExcelFileWithImages(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='excel_files/')
    images= models.ImageField(upload_to="products_items/")




class Item(models.Model):
    id_item= models.CharField(max_length=50,default="0")
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(unique=True,max_length=190)
    article_id=models.CharField(max_length=50)
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=100)
    description_long = models.TextField()
    details = models.CharField(max_length=1500,default="{'color':'black'}")
    tags=models.TextField()
    rating = models.FloatField(blank=True, null=True, 
    validators=[MaxValueValidator(limit_value=5.0)],
        default=0.0)
    gender=models.CharField(choices=LABEL_CHOICES_GENDER, max_length=3,default="M")
    color_exist= models.CharField(max_length=250,default="",blank=True,null=True)
    color_not_exist= models.CharField(max_length=250,default="",blank=True, null=True)
    size_exist= models.CharField(max_length=250,default="34,36,38,40,42",blank=True,null=True)
    size_not_exist= models.CharField(max_length=250, default="",blank=True,null=True)
    wishlist_num = models.FloatField(blank=True, null=True,default=0.0)
    opinion_num = models.FloatField(blank=True, null=True,default=0.0)
    image = models.ImageField()
    
    shipping= models.CharField(max_length=250)
    has_coupon = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=10, blank=True, null=True)
    price_after_coupon= models.FloatField(blank=True, null=True)
    show_coupon = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_added= models.DateTimeField(  default=datetime.datetime.now())
    def __str__(self):
        self.color  = []
        return self.title
    
    def set_has_coupon(self, value):
        self.has_coupon = value
        if value:
            # If has_coupon is True, set a default value for coupon_code
            self.coupon_code = 'DEFAULT_COUPON_CODE'
        else:
            # If has_coupon is False, set coupon_code to None
            self.coupon_code = None

    def save(self, *args, **kwargs):
        # You can add more logic here before saving the instance
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

     

   
 


class ImageItem(models.Model):
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=190 ) 
    image= models.ImageField(upload_to="products/")

    def get_absolute_url(self):
        return reverse("core:imageitem", kwargs={
            'slug': self.slug
        })


    def __str__(self):
        return self.item.title
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, default="")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        if self.item.discount_price:
            return self.quantity * self.item.discount_price
        else:
            return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.price

    def get_amount_saved(self):
        saved_amnt=self.get_total_item_price() - self.get_total_discount_item_price()
        if saved_amnt < 0:
            return -1*saved_amnt
        else:
            return None

    def get_final_price(self):
        if self.item.price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    total_amount= models.IntegerField(default=1)
    recui_image=  models.ImageField(upload_to="orders_recu/",default="",blank=True,null=True)
    phone_number=models.CharField(max_length=10, default="")
    shipping_address = models.CharField(max_length=50,default="")
    shipping_type= models.CharField(max_length=50,default="")
    wilaya_ship=models.CharField(max_length=50, default="")
    commun_ship=models.CharField(max_length=50 , default="")
    shipping_price= models.CharField(max_length=10 , default="")
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"





class WishList(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    items=  models.ManyToManyField(Item)


class TopCategory(models.Model):
    title=models.CharField(max_length=20)
    items=  models.ManyToManyField(Category)
    slug = models.CharField( max_length=190)
    
    def __str__(self):
        return "{} - category".format(self.title) 


class GenderCategory(models.Model):
    title=models.CharField(max_length=20)
    categories=  models.ManyToManyField(TopCategory)
    slug=models.CharField(max_length=190)

    def __str__(self):
        return "{} - gender category".format(self.title)
    
    
    


class Banner_category(models.Model):
    banner_image=models.ImageField(upload_to="banner_imgs")
    banner_link = models.CharField(max_length=500)
    category=  models.ForeignKey(TopCategory,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.category.title
    

class ShopHeader(models.Model):
    shop_header_image=models.ImageField(upload_to="shop_imgs")
    main_title = models.CharField(max_length=50)
    second_title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.main_title
    

class Matacor_info(models.Model):
    email=models.ImageField(upload_to="shop_imgs")
    phone_number = models.CharField(max_length=50)
    ccp = models.CharField(max_length=50)
    name_owner = models.CharField(max_length=50)
    
    def __str__(self):
        return self.main_title