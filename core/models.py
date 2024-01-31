from email.policy import default
from ipaddress import ip_address
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from multiupload.fields import MultiImageField
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'Meilleur vente'),
    ('N', 'Nouveau'),
    ('P', 'Promo')
)

LABEL_CHOICES_EXCEL = (
    ('A', 'ajouter'),
    ('M', 'modifier'),
     
)

LABEL_PAIEMENT = (
    ('E', 'E-paiement'),
    ('C', 'Reçu de Paiement'),
     
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
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default="/static/images/default-avatar.jpg",upload_to="user_profiles")
    fullname=models.CharField(max_length=150,default="")
    email=models.EmailField(max_length=250,default="")
    adresse=models.CharField(max_length=250,default="")
    phone=models.CharField(max_length=20,default="")
    phone=models.CharField(max_length=20,default="")
    reset_code=models.CharField(max_length=6,default="",null=True,blank=True)
    def __str__(self):
        return self.user.username + " profile"


class Slide(models.Model):
    caption1 = models.CharField(max_length=500)
    caption1_en = models.CharField(max_length=500)
    caption1_ar = models.CharField(max_length=500)
    caption2 = models.CharField(max_length=500)
    caption2_en = models.CharField(max_length=500)
    caption2_ar = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    image = models.ImageField(help_text="Size: 1920x570")
    image_mob = models.ImageField(help_text="Size:  ")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)
    
    class Meta:
        verbose_name = "Slide avec text et lien"
        verbose_name_plural = " Slides avec texts et liens"



class Essential(models.Model):
    model_type=models.CharField(max_length=150)
    model_type_en=models.CharField(max_length=150)
    model_type_ar=models.CharField(max_length=150)
    line1 = models.CharField(max_length=500)
    line1_en = models.CharField(max_length=500)
    line1_ar = models.CharField(max_length=500)
    line2 = models.CharField(max_length=500)
    line2_en = models.CharField(max_length=500)
    line2_ar = models.CharField(max_length=500)
    price= models.FloatField()
    button_text= models.CharField(max_length=500)
    button_text_en= models.CharField(max_length=500)
    button_text_ar= models.CharField(max_length=500)
    
    link = models.CharField(max_length=500)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.line1, self.price)
    
    class Meta:
        verbose_name = "banner au centre de la page Home"
        verbose_name_plural = "banners au centre de la page Home"





class Category(models.Model):
    title = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    title_ar = models.CharField(max_length=500)
    slug = models.SlugField(unique=True,max_length=590)
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
     

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })
    
    class Meta:
        verbose_name = "categorie relie à des produit"
        verbose_name_plural = "categories relie à des produit"

class ExcelFile(models.Model):
    name = models.CharField(max_length=500)
    label = models.CharField(choices=LABEL_CHOICES_EXCEL, max_length=1)
    file = models.FileField(upload_to='excel_files/')
    gender = models.CharField(choices=LABEL_CHOICES_GENDER, max_length=3,default="F")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Produits à partir d'un fichier excel"
        verbose_name_plural = "Produits à partir d'un fichier excel"

 



class Item(models.Model):
    id_item= models.CharField(max_length=100,default="0")
    title = models.CharField(max_length=1000)
    title_ar = models.CharField(max_length=1000)
    title_en  = models.CharField(max_length=1000)
    price = models.FloatField(default=0)
    brand_name=models.CharField(max_length=550,default="")
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(unique=True,max_length=590)
    article_id=models.CharField(max_length=100)
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=5000)
    description_long = models.TextField()
    description_long_en = models.TextField()
    description_long_ar = models.TextField()
    # details = models.CharField(max_length=5500,default="{'color':''}")
    details=models.JSONField()
    details_en = models.CharField(max_length=5500,default="{'color':''}")
    details_ar = models.CharField(max_length=5500,default="{'color':''}")
    tags=models.TextField()
    rating = models.FloatField(blank=True, null=True, 
    validators=[MaxValueValidator(limit_value=5.0)],
        default=0.0)
    gender=models.CharField(choices=LABEL_CHOICES_GENDER, max_length=3,default="F")
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
    coupon_start_date = models.DateField(blank=True, null=True)
    coupon_end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_added= models.DateTimeField(  default=datetime.datetime.now())
    def __str__(self):
        self.color  = []
        return self.title
    
    
    

    def is_coupon_valid(self):
        today = timezone.now().date()
        if self.coupon_start_date and self.coupon_end_date:
            return self.coupon_start_date <= today <= self.coupon_end_date
        else:
            return False

    def remaining_days(self):
        today = timezone.now().date()
        remaining_days = (self.coupon_end_date - today).days
        return max(0, remaining_days)
    
    
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
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
     

   
 


class ImageItem(models.Model):
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=590 ) 
    image= models.ImageField(upload_to="products/")

    def get_absolute_url(self):
        return reverse("core:imageitem", kwargs={
            'slug': self.slug
        })


    

    def __str__(self):
        return self.item.title
    
    class Meta:
        verbose_name = "Image de Produit"
        verbose_name_plural = "Images des Produits"
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_per_item=models.FloatField(max_length=200, default=7.0,null=True,blank=True)
    size = models.CharField(max_length=5, default="")
    quantity = models.IntegerField(default=1)
 
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        
        if self.price_per_item == self.item.price_after_coupon:
            
            
            return self.quantity * self.price_per_item
        else:
            self.price_per_item = self.item.price
            
            if self.item.discount_price < self.item.price and self.item.discount_price != self.item.price:
                self.price_per_item = self.item.discount_price
                return self.quantity * self.item.discount_price
            else:
                return self.quantity * self.price_per_item
        

    def get_total_discount_item_price(self):
        if self.price_per_item > self.item.discount_price: 
            return self.quantity * self.item.discount_price
        else:
            return self.quantity * self.price_per_item
            

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

    def save(self,*args,**kwargs):
        self.get_total_item_price()
        super().save(*args, **kwargs)
        
        
        
    class Meta:
        verbose_name = "les produits dans un panier"
        verbose_name_plural = "les Produits dans les paniers"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    formUrl=models.CharField(max_length=1500, default="",blank=True,null=True)

    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    total_amount= models.FloatField(default=1)
    depositAmount= models.FloatField(default=1)
    message=models.CharField(max_length=500, default="",blank=True,null=True)
    ip_address=models.CharField(max_length=500, default="",blank=True,null=True)
    cardholderName=models.CharField(max_length=200, default="",blank=True,null=True)
    approvalCode=models.CharField(max_length=200, default="",blank=True,null=True)
    paiement_meth=models.CharField(choices=LABEL_PAIEMENT, max_length=1)
    recui_image=  models.ImageField(upload_to="orders_recu/",default="",blank=True,null=True)
    phone_number=models.CharField(max_length=10, default="")
    email=models.CharField(max_length=500, default="")
    fullname=models.CharField(max_length=500, default="")
    shipping_address = models.CharField(max_length=50,default="",blank=True, null=True)
    shipping_type= models.CharField(max_length=50,default="",blank=True, null=True)
    wilaya_ship=models.CharField(max_length=50, default="",blank=True, null=True)
    commun_ship=models.CharField(max_length=50 , default="",blank=True, null=True)
    shipping_price= models.CharField(max_length=10 , default="",blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Update modified_at before saving
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    class Meta:
        verbose_name = "la Commande confirmée"
        verbose_name_plural = "les Commandes confirmées"


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=500)
    apartment_address = models.CharField(max_length=500)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=500)
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
    
    class Meta:
        verbose_name = "coupon pour un produit"
        verbose_name_plural = "coupon pour un produit"


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
    
    
    def __str__(self):
        return str(self.user.username)
    class Meta:
        verbose_name = "utilisateur avec sa wishlists"
        verbose_name_plural = "utilisateurs avec leurs wishlists"


class TopCategory(models.Model):
    title=models.CharField(max_length=500)
    items=  models.ManyToManyField(Category)
    slug = models.CharField( max_length=590)
    gender = models.CharField(choices=LABEL_CHOICES_GENDER, max_length=3,default="F")
    def __str__(self):
        return "{} - category".format(self.title)
    class Meta:
        verbose_name = "category ex(Vettements,collections..)"
        verbose_name_plural = "category ex(Vettements,collections..)"
    


class GenderCategory(models.Model):
    title=models.CharField(max_length=20)
    categories=  models.ManyToManyField(TopCategory)
    slug=models.CharField(max_length=50)

    def __str__(self):
        return "{} - gender category".format(self.title)
    
    class Meta:
        verbose_name = "Gender category ex(hommes,femmes..)"
        verbose_name_plural = "Gender category ex(hommes,femmes..)"
    
    
    
class Ad_homePage(models.Model):
    AD_image=models.ImageField(upload_to="AD_imgs")
    AD_link = models.CharField(max_length=500)
    gender=models.CharField(choices=LABEL_CHOICES_GENDER, max_length=3,default="F")
     
    
    def __str__(self):
        return self.AD_link
    
    class Meta:
        verbose_name = "AD home page"
        verbose_name_plural = "AD home page"
    

class Banner_category(models.Model):
    banner_image=models.ImageField(upload_to="banner_imgs")
    banner_link = models.CharField(max_length=500)
    category=  models.ForeignKey(TopCategory,on_delete=models.CASCADE)
    

    
    def __str__(self):
        return self.category.title
    
    class Meta:
        verbose_name = "banner image pour un category ex(vettements, collection)"
        verbose_name_plural = "banner image pour un category  ex(vettements, collection)"
    

class ShopHeader(models.Model):
    shop_header_image=models.ImageField(upload_to="shop_imgs")
    main_title = models.CharField(max_length=50)
    second_title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.main_title
    

class Matacor_info(models.Model):
    email=models.EmailField()
    phone_number = models.CharField(max_length=50)
    ccp = models.CharField(max_length=50)
    name_owner = models.CharField(max_length=50)
    contact_footer=models.TextField(max_length=3000,default="Des questions? Faites-nous savoir en nous envoyant une requête par e-mail ou contactez-nous par téléphone ou à Eurl AllDesigns ain-naadja , algeries, Algeria")
    def __str__(self):
        return self.name_owner
    
    class Meta:
        verbose_name = "Matacor information "
        verbose_name_plural = "Matacor informations (ccp/email,tel...)"
    
    
class Images_upload(models.Model):
    excel_related=models.ForeignKey(ExcelFile, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images_upload_product/')
    
    def __str__(self):
        return "image"
    class Meta:
        verbose_name = "pour l'upload des mutiples images visite /images/upload/"
        verbose_name_plural = "pour l'upload des mutiples images visite /images/upload/"
    

class Faq(models.Model):
    question=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.question
    class Meta:
        verbose_name = "Question & Answer"
        verbose_name_plural = "Questions & Answers"
    
    
class NewsLetterEmails(models.Model):
    email=models.EmailField()
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "NewsLetter Email"
        verbose_name_plural = "NewsLetter Emails"
    
    
class Comments_and_Ratings(models.Model):
    image = models.ImageField(blank=True,default='',upload_to="images_comments")
    rating=models.FloatField(max_length=1)
    comment=models.TextField(max_length=500)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added= models.DateTimeField(  default=datetime.datetime.now())
    def __str__(self):
        return "comment of {} on product N° {}".format(self.user,self.product.id)
    
    class Meta:
        verbose_name = "commentaire de chaque produit"
        verbose_name_plural = "commentaires de chaque produit"
    
class Comment_images(models.Model):
    image = models.ImageField(default='',upload_to="images_comments")
    comment=models.ForeignKey(Comments_and_Ratings,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return "image comment of {}".format(self.user)
    
    class Meta:
        verbose_name = "image de commentaire"
        verbose_name_plural = "les images des commentaires"