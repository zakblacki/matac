from itertools import product
from urllib import request
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import *
from .models import *
from django.http import HttpResponseRedirect
import ast
from django.db.models import Q
from django.forms.models import model_to_dict
from .serializers import *
from rest_framework import generics
# Create your views here.
import random
import string
import stripe
from django.contrib.auth import authenticate, login , logout
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
stripe.api_key = settings.STRIPE_SECRET_KEY
import requests
from django import template
import json
import os
import shutil
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt decorator if needed

register = template.Library()

@register.filter
def split_and_length(value, delimiter):
    # Split the string using the given delimiter and return its length
    return len(value.split(delimiter))


def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def custom_server_error_view(request):
    return render(request, '500.html', status=500)

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


 

class PaymentView(View):
     
    def post(self, *args, **kwargs):
        form = FormInput(self.request.POST or None)
        
        if form.is_valid():
         
            return redirect("/")


class HomeView(ListView):
    template_name = "index.html"
    model= Item
    context_object_name = 'items'
     
    
    def get_queryset(self):
        # Get all products
        all_products = list(Item.objects.all(is_active=True))
        # Get a random selection of products
        items = random.sample(all_products, 1)
        
        return items



def login_view(request): 
    if request.method == 'POST':
        print("try............")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("try")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user is not None:
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')  # Redirect to the home page after successful login
            else:
                pass
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})


def register_view(request):
     
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
          
            
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user = form.save(commit=False)
                
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return redirect('core:login_')
            else:
                
                return redirect('core:register_')
         
            
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})



def wishlist_add_view(request,slug):
    item = get_object_or_404(Item, slug=slug)
    
    
    if request.user.is_authenticated:
        if item:
            try:
                user_wish = WishList.objects.filter(user=request.user)
            except:
                user_wish=[]
            if user_wish.first():
                
                user_wish =user_wish.first()
                if item in user_wish.items.all():
                    
                    user_wish.items.remove(item)
                    item.wishlist_num = item.wishlist_num - 1
                     
                    if item.wishlist_num <0:
                        item.wishlist_num =0
                    item.save()
                else:
                    user_wish.items.add(item)
                    item.wishlist_num = item.wishlist_num + 1
                    
                    item.save()
                    
                 
            else:
                WishList.objects.create(
                    user= request.user,
                     
                )
                item.wishlist_num = item.wishlist_num + 1
                item.save()
                WishList.objects.get(
                    user= request.user,
                ).items.add(item)
             
                
        else:
            return redirect("wishlist")
        
        return redirect(f"/product/{slug}/")
    else:
        return redirect("/accounts/login")
     

def logout_view(request):
    logout(request)
    return redirect('/')

def wishlist_view(request):
     
    
 
    
    context={}
    try:
        if request.user.is_authenticated:
            try:
                user_wish=WishList.objects.filter(user=request.user).first()
            except:
                user_wish=[]
            if len(user_wish.items.all())>0:
                context["wishlists"]=user_wish.items.all()
                return render(request, 'wishlist.html' ,context)
            else:
                return redirect("/")
        else:
            return redirect("/")
        
            
    except:
    
        return redirect("/")



def index(request):
    
    try:
        email_news=request.GET["email_newsletter"]
        NewsLetterEmails.objects.create(email=email_news)
        
    except:
        pass

    try:
        tp=request.GET["gender"]
    except:
        tp="F"
    
    # Get a random selection of products
    try:
        items_most_sales = random.sample(list(Item.objects.filter(label="S",is_active=True,gender=tp)),32)
    except:
        items_most_sales = Item.objects.filter(label="S",is_active=True,gender=tp)
    try:
        items_most_new = random.sample(list(Item.objects.filter(label="N",is_active=True,gender=tp)), 32)
    except:
        items_most_new =  Item.objects.filter(label="N",is_active=True,gender=tp) 
    try:
        items_promo= random.sample(list(Item.objects.filter(label="P",is_active=True,gender=tp)), 32) 
    except:
        items_promo=Item.objects.filter(label="P",is_active=True,gender=tp)
    try:
        wishlist =WishList.objects.get(user=request.user).items.all()
    except:
        wishlist=[]
    

    
    
    
    context={
        "items":Item.objects.filter(is_active=True,gender=tp),
        "category":Category.objects.filter(is_active=True),
        "category_gen":TopCategory.objects.filter(gender=tp),
        "new_items":items_most_new,
        "promo_items":items_promo,
        "most_sale":items_most_sales,
        "essentials":Essential.objects.filter(is_active=True),
        "wishedlist":wishlist,
        "ad_items":Ad_homePage.objects.filter(gender=tp)[:2]
    }
    
    print(context)
    return render(request, 'index.html',context) 


 
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        
        if len(OrderItem.objects.filter(user=self.request.user, ordered=False)) !=0:
            try:
                order = OrderItem.objects.filter(user=self.request.user, ordered=False)
                try:  
                    print("cupon: ", self.request.GET["code_coupon"])
                    for order1 in order.all():
                        if order1.item.coupon_code == self.request.GET["code_coupon"]:
                            order1.price_per_item=order1.item.price_after_coupon
                            order1.save()
                            
                except:
                    pass
                context = {
                    'object': order,
                    "orderid":order.first().id,
                    "form":FormInput(),
                    "contact":Matacor_info.objects.first()
                }
                return render(self.request, 'order_summary.html', context)
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order")
                return redirect("/")
        else:
            return redirect("/")

    def post(self, *args, **kwargs):
        form = FormInput(self.request.POST,self.request.FILES)
        
        
        if form.is_valid():
             
            
        
            phone=form.cleaned_data.get("phone") 
            email=form.cleaned_data.get("email")
            address=form.cleaned_data.get("address")
            fullname=form.cleaned_data.get("fullname")
            wilaya=form.cleaned_data.get("wilayaship")
            commun=form.cleaned_data.get("communship")
            deliverytype=form.cleaned_data.get("delivery_type")
            deliveryprice=form.cleaned_data.get("delivery_price")

           
                
            
             
                
            
           
        
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.ref_code:
                    confirmorderapi="https://test.satim.dz/payment/rest/confirmOrder.do?language=EN&orderId={}&password=satim120&userName=SAT2310130762".format(order.ref_code)
                    orderidpai=requests.get(confirmorderapi)
                    try:
                        if orderidpai.json()["depositAmount"] == order.get_total():
                            order.ordered = True
                            order.approvalCode = orderidpai.json()["approvalCode"]
                            for item_ordered in order.items.all():
                                item_ordered.ordered = True
                                item_ordered.save() 

                    except:
                        pass
            amount = int(order.get_total() * 100)
            try:
                order.commun_ship = commun
                order.wilaya_ship = wilaya
                order.email=email
                order.fullname=fullname
                order.shipping_type = deliverytype
                order.shipping_price= deliveryprice
                
                # orderidpai=requests.get("https://test.satim.dz/payment/rest/register.do?currency=012&amount="+str(amount)+"&language=fr&orderNumber="+ str(order.id)+"&userName=SAT2310130762&password=satim120&returnUrl=https://matacor.com/fr/confirm_order/" +str(order.user.username) +  "/"+str(order.id) + "/directpayment/step2/cib%3Flogin%3Dtest%26variable%3DtestPwd&failUrl=https://matacor.com/fr/confirm_order/" +str(order.user.username) +  "/"+str(order.id) +  "/directpayment/step2/cib/c&jsonParams={'force_terminal_id':'E005005097','udf1':'2018105301346','udf5':'ggsf85s42524s5uhgsf'}")
                # Get the current date and time in UTC
                 
                objtest='{"force_terminal_id":"E010901004","udf1":"20231221","udf5":"ggsf85s42524s5uhgsf"}'
                strapi="https://test.satim.dz/payment/rest/register.do?currency=012&amount={}&language=fr&orderNumber={}&userName=SAT2310130762&password=satim120&returnUrl=https://matacor.com/payement_status/{}/&failUrl=https://matacor.com/payement_status/{}/&jsonParams={}".format(str(amount),str(order.id),str(order.id),str(order.id),objtest)
                orderidpai=requests.get(strapi)
                # order.ref_code = create_ref_code()*
                try :
                    if orderidpai.json()["orderId"] and orderidpai.json()["errorCode"] != '1':
                        order.ref_code =orderidpai.json()["orderId"]
                        
                        order.formUrl =orderidpai.json()["formUrl"]
                except:
                    return redirect("/order-summary/")

                
                

                
                
                    
                    
                  
                
                order.total_amount=order.get_total()
                order.phone_number=phone
                order.shipping_address = address
                if form.cleaned_data.get("recu_img"):
                    img=form.cleaned_data.get("recu_img")
                    order.recui_image = img
                    order.ordered = True
                    for item_ordered in order.items.all():
                        item_ordered.ordered = True
                        item_ordered.save() 
                
                
                order.save()

                
                try:
                    return redirect("/confirm_order/{}/{}/".format(self.request.user,order.id))
                    # messages.success(self.request, "Order was successful")
                except:
                    return redirect("/order-summary/")
                    # messages.error(self.request, "Something went wrong")
            
                # return redirect("/confirm_order/{}/{}/".format(self.request.user,order.id))

        
                # Display a very generic error to the user, and maybe send
                # yourself an email
               
                

            except  :
                # send an email to ourselves
                messages.error(self.request, "Serious Error occured")
        else:
            return redirect("/order-summary/")



class ShopView(ListView):
    model = Item
    paginate_by = 24
    template_name = "shop.html"
    
    def get(self, *args, **kwargs):  
        searchtext=""
        filtermeth=""  
        brand_qry=Q()
        topcatsearch=Q()
        color=None
        color_q=Q()
        try:
            
            
        
            # Check if the lookup is a valid field in the model
            
                # Create Q objects for each value and combine them using OR (|)
            if len(self.request.GET)>0: 
                min_price_query=10
                max_price_query=10
                combined_query=Q()
                combined_query1=Q()
                combined_query2=Q()
                combined_query3=Q()
                combined_query5=Q()
                # combined_color=Q()
                query_srch=Q()
                
                 
                
                for get_key, get_val in self.request.GET.items():
                    model_instance = Item()
                    model_dict = model_to_dict(model_instance)
                    
                    # Get the keys of the dictionary, which are the field names
                    field_names = list(model_dict.keys())
                    
                    
                    lookup = f"{get_key}__icontains"
                    
                    if get_key in field_names:
                        
                        if get_key =="gender":
                            lookup="gender__iexact"
                            
                            
                            combined_query |= Q(**{lookup: get_val})
                            
                        if get_key =="size_exist":
                        
                            combined_query5 |= Q(**{lookup: get_val})
                    else:
                        
                        if get_key == "search":
                            searchtext=get_val
                            
                            if get_val != "" :
                                
                                query_srch |= Q(title__icontains=get_val)
                                query_srch |= Q(article_id__icontains=get_val)
                                query_srch |= Q(id_item__icontains=get_val)
                        else:
                            pass
                            
                            
                    
                        
                        if "start" in get_key and get_val != '' :
                            
                            min_price_query = Q(price__gte=float(get_val))
                            
                            combined_query1= min_price_query
                            
                            
                        if "end" in get_key and get_val != '' and get_val != 0:
                            
                            max_price_query = Q(price__lte=float(get_val))
                            
                            combined_query2= max_price_query
                        
                        if "filter" == get_key:
                            filtermeth=get_val   
                        
                        if combined_query1 and combined_query2:
                            combined_query3 |=combined_query1 & combined_query2
                            
                        if "brand" == get_key:
                            brand_qry |=Q(brand_name__iexact=get_val)
                           
                            combined_query3 |= brand_qry
                        
                        if "color" == get_key:
                             
                            color_q |= Q(tags__icontains=get_val)
                            
                          
                        
                        
                        if "topcat" == get_key:
                            separted=get_val.split('_')
                            
                            for valslug in separted[1:]:
                                catitem =Category.objects.filter(slug=valslug).first()
                                topcatsearch |= Q(category=catitem)
                                
                                 
                                

                                
                            
                    
                if query_srch :
                    
                    comb_final = query_srch & combined_query & combined_query5 & combined_query3
                else:
                    comb_final = combined_query & combined_query5 & combined_query3
                
                if brand_qry:
                    comb_final = comb_final & brand_qry
                
                

                if color_q:
                    comb_final= comb_final & color_q
                    item =self.get_queryset().filter(comb_final,is_active=True)

                if topcatsearch :
                    
                    comb_final = comb_final & topcatsearch
                item= self.get_queryset().filter(comb_final,is_active=True)
                 
                if filtermeth:
                     
                    
                    item =self.get_queryset().filter(comb_final,is_active=True).order_by(filtermeth)
                else:
                    pass
            else:
                item = self.get_queryset().filter( is_active=True)
                 

        except:
            item = self.get_queryset().filter( is_active=True)
        
        if color:
            listupdated= []
            color=color.split("-")
            for clr,itm in zip(color,item):
                if clr in itm.details :
                    listupdated.append(itm)
                    
            item=listupdated
        
        try:
            page_number = int(self.request.GET.get('page'))
        except:
            page_number=1
            
        paginator = Paginator(item, self.paginate_by)
        paginated_items = paginator.get_page(page_number)
        brands_list=list(Item.objects.values_list('brand_name', flat=True).distinct())
        paginated_items.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
     
        context = {
            'object_list_len': item,
            'object_list': paginated_items,
             'categories':Category.objects.all(),
             'header':ShopHeader.objects.first(),
             'brands_list':brands_list,
             "searchtext":searchtext
        }
        if  self.request.user.is_authenticated:
          
          
            # context["wishlist"]=WishList.objects.filter(user=self.request.user).first().items.all()
            try:
                context["wishlist"]=list(WishList.objects.filter(user=self.request.user).first().items.all())
            except:
                context["wishlist"]= None
        else:
            context["wishlist"]=None
        
        return render(self.request, "shop.html", context)             



 
@csrf_exempt
def ajax_example(request):
    if request.method == 'POST':
        print(request.FILES.getlist('images'))
        data = {'message': 'This is a POST AJAX response'}
        return JsonResponse(data)
    return JsonResponse({'message': 'Invalid Request'}, status=400)


def ajax_example(request):
    if request.method == 'POST':
      
        form = ImageUploadForm(request.POST, request.FILES)
        print('form')
        if form.is_valid():
            print('requested')
            title= int(request.POST['excel_related'])
            for index,image in enumerate(request.FILES.getlist('images')):
                
                print("uploading..",(index+1)*100/len(request.FILES.getlist('images')))
                if image:
                    if image :
                        
                        parts = image.name.split("_")[-1]
                        folder_name_org=parts.split(".")[0]
                        name_org=str(image.name.split("_")[-2]) + "_org_zoom" + ".webp"
                        
                        
                        # Construct the path to the media_root directory
                        media_root1 = os.path.join(settings.MEDIA_ROOT, "images_upload_product" , folder_name_org)
                        media_root21 = os.path.join(settings.MEDIA_ROOT, "images_upload_product" , "doubled_must_delted")
                        # Create the 'images' directory if it doesn't exist
                        
                        os.makedirs(media_root1, exist_ok=True)
                        os.makedirs(media_root21, exist_ok=True)
                        image_path_up = os.path.join(media_root1,name_org)
                        realimg_path= os.path.join(settings.MEDIA_ROOT, "images_upload_product",name_org )
                        realimg_path_exact= os.path.join( settings.MEDIA_ROOT,"images_upload_product",folder_name_org,name_org )
                        
                        image.name= name_org
                        
                    

                        if not os.path.exists(image_path_up):
                            imageup=Images_upload.objects.create(excel_related_id=title, images=image )
                            try:
                                shutil.move(realimg_path, media_root1)
                            except:
                                shutil.move(realimg_path, media_root21)
                            imageup.images=realimg_path_exact.replace("/workspace/media_root","")
                            imageup.save()
                            
                
                else:
                    pass
                    
            # form.save()
        return redirect("/ss")
    else:
        form = ImageUploadForm()
    return render(request,"admin/upload.html",{"form":form})

def admin_upload(request):
    if request.method == 'POST':
        print('form')
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('requested')
            title= form.cleaned_data['excel_related']
             

            for index,image in enumerate(request.FILES.getlist('images')):
                 
                # print("uploading..",(index+1)*100/len(request.FILES.getlist('images')))
                try:
                   
                       
                        
                    parts = image.name.split("_")[-1]
                    idimg = image.name.split("+")[0]

                        
                    folder_name_org=parts.split(".")[0]
                    image_number=index
                    # name_org=str(image.name.split("_")[-2]) + "_org_zoom" + ".webp"
                    name_org=  idimg +str(image).replace(idimg,"")

                    folder_name_org = os.path.join(  folder_name_org,str(image_number))
                        
                        # Construct the path to the media_root directory
                    media_root1 = os.path.join(settings.MEDIA_ROOT, "images_upload_product"  )
                    media_root21 = os.path.join(settings.MEDIA_ROOT, "images_upload_product" , "doubled_must_delted")
                        # Create the 'images' directory if it doesn't exist
                        
                    os.makedirs(media_root1, exist_ok=True)
                    os.makedirs(media_root21, exist_ok=True)
                    image_path_up = os.path.join(media_root1,name_org)
                    realimg_path= os.path.join(settings.MEDIA_ROOT, "images_upload_product",name_org )
                    realimg_path_exact= os.path.join( settings.MEDIA_ROOT,"images_upload_product",name_org )
                        
                        # image.name= name_org
                        
                    
                    cur_prod=Item.objects.filter(id_item=idimg).first()
                    if not os.path.exists(image_path_up) and cur_prod:
                        imageup=Images_upload.objects.create(excel_related=title, images=image )
                            # try:
                            #     shutil.move(realimg_path, media_root1)
                            # except:
                            #     shutil.move(realimg_path, media_root21)

                        imageup.images=realimg_path_exact.replace("/workspace/media_root","").replace("+","").replace("/root/demo/media_root","")
                            
                        imageup.save()
                        if imageup:
                            imageup1=ImageItem.objects.create(item=cur_prod,slug=cur_prod.slug,image=image)
                                # try:
                                #     shutil.move(realimg_path, media_root1)
                                # except:
                                #     shutil.move(realimg_path, media_root21)
                                
                            imageup1.image=realimg_path_exact.replace("/workspace/media_root","").replace("+","").replace("/root/demo/media_root","")
                                
                            imageup1.save()
                            first_img = "+0"
                            sec_img = "+1"

                            if first_img in realimg_path_exact:
                                cur_prod.image=realimg_path_exact.replace("/workspace/media_root","").replace("+","").replace("/root/demo/media_root","")
                            elif sec_img in realimg_path_exact:
                                cur_prod.image=realimg_path_exact.replace("/workspace/media_root","").replace("+","").replace("/root/demo/media_root","")
                            else:
                                cur_prod.image=realimg_path_exact.replace("/workspace/media_root","").replace("+","").replace("/root/demo/media_root","")

                            cur_prod.save()
                        else:
                            pass


                   
                            
                    
                except:
                    pass    
            # form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        form = ImageUploadForm()
    return render(request,"admin/upload.html",{"form":form})

 
def profile(request):

    if request.user.is_authenticated:
    
    
        if request.method == "POST":
            fullname=request.POST["first_name"]
            phone=request.POST["phone"]
            email=request.POST["email"]
            picture=request.FILES.get("picture")
            address=request.POST["address"]
            
            try:
                prodifile = Profile.objects.get(user=request.user)
                if fullname:
                    prodifile.fullname=fullname
                if phone:
                    prodifile.phone=phone
                if email:
                    prodifile.email=email
                if picture:
                    prodifile.image=picture
                if address:
                    prodifile.adresse=address
                    
                prodifile.save()
                print(prodifile)
            except:
                Profile.objects.create(user=request.user,
                                    fullname=fullname,
                                    image=picture,
                                    email=email,
                                    adresse=address,
                                    phone=phone)
                
            
        
        else:
            pass
            
            
    
        
        ordered= Order.objects.filter(user=request.user,ordered=True)
        products_com= Comments_and_Ratings.objects.filter(user=request.user)
        context={
            "lengg":len(products_com),
            "leng":len(ordered),
            "products_com":products_com,
            "orders":ordered }
        return render(request,"profile.html",context)
    else:
        return redirect("/accounts/login")

 
def confirmorder(request,slug,slug1):
    if request.user.is_authenticated:
    
        context={}
        
        
        ordertar= None
        context={}
        
        context["contact"]=Matacor_info.objects.first()
        
        if str(slug.replace(" ","")) == str(request.user):
        
            ordertar=get_object_or_404(Order, id=int(slug1))
            
            
            context["target"]=ordertar
            


        order= get_object_or_404(Order, id=int(slug1))
        if order.ref_code:
            confirmorderapi="https://test.satim.dz/payment/rest/confirmOrder.do?language=EN&orderId={}&password=satim120&userName=SAT2310130762".format(order.ref_code)
            orderidpai=requests.get(confirmorderapi)
            try:
                if orderidpai.json()["depositAmount"] == order.get_total()*100:
                    order.ordered = True
                    order.depositAmount=orderidpai.json()["depositAmount"]/100
                    order.message=orderidpai.json()["actionCodeDescription"]
                    order.ip_address=orderidpai.json()["Ip"]
                    order.cardholderName=orderidpai.json()["cardholderName"]
                    order.approvalCode = orderidpai.json()["approvalCode"]
                    order.paiement_meth="E"
                    for item_ordered in order.items.all():
                        item_ordered.ordered = True
                        item_ordered.save() 
                    order.save()
                else:
                    order.paiement_meth="C"
            except:
                order.paiement_meth="C"
                order.save()
            
            
        if request.method == "POST":
            
            context["form"]=UploadImg(request.POST,request.FILES)
            context["formConf"]=NotRobot(request.POST)

            if context["formConf"].is_valid():
                if order.ref_code:
                    return redirect(f"https://test.satim.dz/payment/merchants/merchant1/payment_fr.html?mdOrder={order.ref_code}")
                else:
                    return redirect("/")
                
            if context["form"].is_valid():
                
                
                
                
                ordertar.recui_image = request.FILES.get("recu_img")
                ordertar.ordered=True
                for item_ordered in ordertar.items.all():
                    item_ordered.ordered = True
                    item_ordered.save()  
                
                ordertar.save()
                # ordertar.recui_image = img
                # ordertar.save()
        else:
            context["form"]=UploadImg()
            context["formConf"]=NotRobot()
        
        
        return render(request,"confirm_order.html",context)
    else:
        return redirect("/accounts/login")

import ast
class ItemDetailView(DetailView):
    model = Item

    template_name = "product-detail.html"
    
    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            form=ImageUploadForm1(self.request.POST,self.request.FILES)
           
            findslug=self.request.POST["findslug"]
            comment=self.request.POST["text"]
            rate=self.request.POST["rating"]
            imagee=self.request.POST["allcomimagesin_one"]
            com_img=self.request.FILES.get("image")
            print(com_img)
            product_tar=Item.objects.get(slug=findslug)
            if not rate:
                rate=0
            if not comment:
                comment=""
            try:
                print("commented")
                targetcomment=Comments_and_Ratings.objects.create(
                    user=self.request.user,
                    rating=rate,
                    comment=comment,
                    product=product_tar,
                    image=com_img
                )
                 
                     
               
                Comment_images.objects.create(
                    user=self.request.user,
                    image= com_img ,
                    comment=targetcomment,
                    
                )
            except:
                pass
            
            
            return redirect("/")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # Add additional data to the context
        context['images'] =ImageItem.objects.filter(slug=self.object.slug) 
        
        

        details_json = getattr(self.object, 'details', None)

        # Check if details_json is not None and not an empty string
        if details_json and isinstance(details_json, str):
            
            context['details'] = json.loads(details_json)
            
        else:
            context['details'] = {}
        
        # context["details"] = json.loads(self.object.details )
        
            
        context["comments"] =   Comments_and_Ratings.objects.filter(product=self.object.id)
        
        context["colors_item"] = Item.objects.filter(article_id=self.object.article_id)
        context["form"]=ImageUploadForm1()
        if  self.request.user.is_authenticated:
            try:
                if self.object in WishList.objects.get(user=self.request.user).items.all():
                
                    context["whished"]=True
                else:
                    context["whished"]=False
            except:
                pass
        else:
            context["whished"]=None
        
        relateditems = Item.objects.filter(category=self.object.category).exclude(pk=self.object.pk)
        context["bought"]=False
        if self.request.user.is_authenticated:

            # objectsbought=Order.objects.filter(user=self.request.user)
            
            # if self.object in objectsbought.items.all():
            #     context["bought"]=True
            orders_with_product = Order.objects.filter(items__item=self.object,items__ordered=True)

            # Set the 'bought' variable based on whether the product is in any order
            context['bought'] = orders_with_product.exists()




        if len(relateditems) < 5 :
            objecttags=self.object.title.split(" ")
            
               
            similar_items_q = Q() # # Get the initial QuerySet of products
            for item in objecttags:
                similar_items_q |= Q(tags__icontains=item)
            
            initial_queryset = Item.objects.filter(similar_items_q).exclude(pk=self.object.pk)
            context["relate_pros"] = initial_queryset
            
            
            if len(initial_queryset) <= 4:
                for item in objecttags:
                    similar_items_q |= Q(tags__icontains=item)
                    similar_items_q2 = Q(description_long__icontains=item)
                combined_q = similar_items_q | similar_items_q2
                initial_queryset = Item.objects.filter(combined_q).exclude(pk=self.object.pk)

            try:
                context["relate_pros"] = random.sample(list(initial_queryset),24)
            except:
                pass
             
            
         
        else:
            try:
            
                context["relate_pros"] = random.sample(list(Item.objects.filter(category=self.object.category).exclude(pk=self.object.pk)) ,24) 
            except:
                context["relate_pros"] =  Item.objects.filter(category=self.object.category).exclude(pk=self.object.pk) 

           
           
         
        
        # Get all comments related to the post
        return context

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
class CategoryView(ListView):
    model = Item
    paginate_by = 24
    template_name = "category.html"
     
    
    
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        combined_query = Q()
        topcatsearch=Q()
        filtermeth=""
        bannertarg=[]
        banners=[]
        brand_qry=Q()
        color_q=Q()
       
        for cattg in TopCategory.objects.filter(items__title=category):
            if len(Banner_category.objects.filter(category__title=cattg.title))>0:
                if category in cattg.items.all():
                    
                    for itmc in Banner_category.objects.filter(category__title=cattg.title):
                        banners.append(itmc)
                    
                # bannertarg=Banner_category.objects.filter(category__title=cattg.title)
                 
                # banners=bannertarg
                
            # for catt in TopCategory.objects.filter(items__title=category):
                
                
           
                
        try:
            
        
            # Check if the lookup is a valid field in the model
            
                # Create Q objects for each value and combine them using OR (|)
            if len(self.request.GET)>0: 
                min_price_query=10
                max_price_query=10
                combined_query=Q()
                combined_query1=Q()
                combined_query2=Q()
                combined_query3=Q()
                combined_query5=Q()
                
                
                for get_key, get_val in self.request.GET.items():
                    model_instance = Item()
                    model_dict = model_to_dict(model_instance)
                    
                    # Get the keys of the dictionary, which are the field names
                    field_names = list(model_dict.keys())
                    
                    
                    lookup = f"{get_key}__icontains"
                    
                    if get_key in field_names:
                        
                        if get_key =="gender":
                            lookup="gender__iexact"
                            
                            
                            combined_query |= Q(**{lookup: get_val})
                            
                        if get_key =="size_exist":
                        
                            combined_query5 |= Q(**{lookup: get_val})
                    else:
                    
                        
                        if "start" in get_key and get_val != '' :
                            
                            min_price_query = Q(price__gte=float(get_val))
                            
                            combined_query1= min_price_query
                            
                            
                        if "end" in get_key and get_val != '' and get_val != 0:
                            
                            max_price_query = Q(price__lte=float(get_val))
                            
                            combined_query2= max_price_query
                            
                        if "filter" == get_key:
                            filtermeth=get_val
                            
                        if "brand" == get_key:
                            brand_qry |= Q(brand_name__iexact=get_val)

                        if "color" == get_key:
                            color_q |= Q(tags__icontains=get_val)
                        
                        
                        
                             
                            
                        if combined_query1 and combined_query2:
                            combined_query3 |=combined_query1 & combined_query2
                            
                        
                            
                            
                            
                
                        
                combined_cat = Q(category__title=category.title)
                
                
                comb_final  =   combined_query & combined_query5 & combined_query3 & combined_cat
                 
                
                item= self.get_queryset().filter(comb_final,is_active=True)
                if brand_qry:
                    comb_final= comb_final & brand_qry
                    item =self.get_queryset().filter(comb_final,is_active=True)

                if color_q:
                    comb_final= comb_final & color_q
                    item =self.get_queryset().filter(comb_final,is_active=True)
                    
                if filtermeth:
                     
                    
                    item =self.get_queryset().filter(comb_final,is_active=True).order_by(filtermeth)
                else:
                    pass
                
                
                    
            else:
                
                item = self.get_queryset().filter(category=category, is_active=True)
                 

        except:
            item = self.get_queryset().filter(category=category, is_active=True)
             
       
            
         
        try:
            page_number = int(self.request.GET.get('page'))
        except:
            page_number = 1
        
        paginator = Paginator(item, self.paginate_by)
        paginated_items = paginator.page(page_number)
        paginated_items.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
        listbrand=list(Item.objects.values_list('brand_name', flat=True).distinct())
       
        context = {
            'object_list_len': item,
            'object_list': paginated_items,
            'brand_list':listbrand,
            'category_title': category,
            'category_description': "",
            'category_image': category.image.url,
            'banners':banners,
            'categories':Category.objects.all()
        }
        if  self.request.user.is_authenticated:
          
          
            # context["wishlist"]=WishList.objects.filter(user=self.request.user).first().items.all()
            try:
                context["wishlist"]=list(WishList.objects.filter(user=self.request.user).first().items.all())
            except:
                context["wishlist"]=[]
        else:
            context["wishlist"]=None
        return render(self.request, "category.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = FormInput(self.request.POST or None)
        
        if form.is_valid():
            
        
            phone=form.cleaned_data.get("phone") 
            email=form.cleaned_data.get("email")
            address=form.cleaned_data.get("address")
            fullname=form.cleaned_data.get("fullname")
             
            img=form.cleaned_data.get("recu_img")
            
         
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.ref_code:
                confirmorderapi="https://test.satim.dz/payment/rest/confirmOrder.do?language=EN&orderId={}&password=satim120&userName=SAT2310130762".format(order.ref_code)
                orderidpai=requests.get(confirmorderapi)
                try:
                    if orderidpai.json()["depositAmount"] == order.get_total():
                        order.ordered = True
                        order.approvalCode = orderidpai.json()["approvalCode"]
                        for item_ordered in order.items.all():
                            item_ordered.ordered = True
                            item_ordered.save() 

                except:
                    pass
            amount = int(order.get_total() * 100)
            try:
                current_datetime = timezone.now()

                # Format the date and time as a string in the desired format
                formatted_datetime = current_datetime.strftime('%Y%m%d%H%M%S%f')[:-3]

                objtest=f'{"force_terminal_id":"E010901004","udf1":{str(formatted_datetime)},"udf5":"ggsf85s42524s5uhgsf"}'
                # orderidpai=requests.get("https://test.satim.dz/payment/rest/register.do?currency=012&amount="+str(amount)+"&language=fr&orderNumber="+ str(order.id)+"&userName=SAT2310130762&password=satim120&returnUrl=https://matacor.com/fr/confirm_order/" +str(order.user.username) +  "/"+str(order.id) + "/directpayment/step2/cib%3Flogin%3Dtest%26variable%3DtestPwd&failUrl=https://matacor.com/fr/confirm_order/" +str(order.user.username) +  "/"+str(order.id) +   "/directpayment/step2/cib/c&jsonParams={'force_terminal_id':'E005005097','udf1':'2018105301346','udf5':'ggsf85s42524s5uhgsf'}")
                # objtest='{"force_terminal_id":"E010901004","udf1":"20231017301346","udf5":"ggsf85s42524s5uhgsf"}'
                strapi="https://test.satim.dz/payment/rest/register.do?currency=012&amount={}&language=fr&orderNumber={}&userName=SAT2310130762&password=satim120&returnUrl=https://matacor.com/status/{}/&failUrl=https://matacor.com/status/{}/&jsonParams={}".format(str(amount),str(order.id),str(order.id),str(order.id),objtest)
                orderidpai=requests.get(strapi)
                # order.ref_code = create_ref_code()*
                try :
                    if orderidpai.json()["orderId"] and orderidpai.json()["errorCode"] != '1':
                        order.ref_code =orderidpai.json()["orderId"]
                        order.formUrl =orderidpai.json()["formUrl"]
                except:
                    order.ref_code=create_ref_code()
                
                
                
                
                
                 
                    
                    
                 
                
                order.total_amount=order.get_total()
                order.phone_number=phone
                order.shipping_address = address
                if img:
                    for item_ordered in order.items.all():
                        item_ordered.ordered = True
                        item_ordered.save()  
                    order.ordered = True
                    order.recui_image = img
                
                     
                
                
                
                order.save()

                
                try :
                    if orderidpai.json()["orderId"] and orderidpai.json()["errorCode"] != '1':
                        return redirect("/confirm_order/{}/{}/".format(self.request.user,order.id))
                    # messages.success(self.request, "Order was successful")

                except:
                    # messages.error(self.request, "Something went wrong")
                    return redirect("/order-summary/")

        
                # Display a very generic error to the user, and maybe send
                # yourself an email
               
                

            except  :
                # send an email to ourselves
                messages.error(self.request, "Serious Error occured")
        else:
            return redirect("/")



 

 
def add_to_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        
        size= request.GET["search"]
    
        
        
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
            size=size
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Item qty was updated.")
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "Item was added to your cart.")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date,)
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
        return redirect("core:order-summary")
    else:
        return redirect("/accounts/login")


def refund(request, id_ref):
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(pk=id_ref,user=request.user,).first()
        amounttot=int(order_qs.depositAmount)*100
        confirmorderapi="https://test.satim.dz/payment/rest/refund.do?amount={}&language=AR&orderId={}&password=satim120&userName=SAT2310130762".format(amounttot,order_qs.ref_code)
        orderidpai=requests.get(confirmorderapi)
        
        if orderidpai.json()["errorMessage"] == "Success":
            
            # for item_ordered in order_qs.items.all():
            #     item_ordered.delete()
            #     item_ordered.save() 
            order_qs.items.clear()
            order_qs.save()
            order_qs.delete()

    
    
    
        return redirect("/profile")
    else:
            return redirect("/accounts/login")

    

 
def remove_from_cart(request, slug):
    if request.user.is_authenticated:


   
        size=request.GET["search"]
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False,
                    size=size
                )[0]
                
                # order.items.remove(order_item)
                order_item.delete()
                if len(order.items.all()) == 0:
                    order.delete()

                messages.info(request, "Item was removed from your cart.")
                return redirect("core:order-summary")
                # return JsonResponse({str(order_item):str(len(order.items.all()) )}, status=400)
            else:
                # add a message saying the user dosent have an order
                messages.info(request, "Item was not in your cart.")
                return redirect("core:product", slug=slug)
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "u don't have an active order.")
            return redirect("core:product", slug=slug)
        return redirect("core:product", slug=slug)
    else:
        return redirect("/accounts/login")

 
def remove_single_item_from_cart(request, slug):
    
    if request.user.is_authenticated:
     
        size=request.GET["search"]
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False,
                    size=size
                )[0]


                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                
                else:
                    order_item.delete()
                    order.items.remove(order_item)
                if len(order.items.all()) == 0:
                    order.delete()
                messages.info(request, "This item qty was updated.")
                return redirect("core:order-summary")
            else:
                # add a message saying the user dosent have an order
                messages.info(request, "Item was not in your cart.")
                return redirect("core:product", slug=slug)
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "u don't have an active order.")
            return redirect("core:product", slug=slug)
        return redirect("core:product", slug=slug)

    else:
                return redirect("/accounts/login")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")



from django.http import JsonResponse
def testt(request):
    # Render your main index template here
    return render(request, "testt.html")



def get_filtered_items_by_type(filter_type):
    if filter_type == "category":
        # Filter items by category and serialize them
        filtered_items = Category.objects.filter(title="selected_category").values()
    elif filter_type == "price":
        # Filter items by price and serialize them
        filtered_items = Item.objects.filter(price__lte=selected_price).values()
    elif filter_type == "gender":
        # Filter items by gender and serialize them
        filtered_items = Item.objects.filter(gender="selected_gender").values()
    else:
        filtered_items = []

    return list(filtered_items)


def get_filtered_items(request):
    
    filter_type = request.GET.get("filter")
    
    # Retrieve and filter items based on the selected filter_type
    # Return the filtered items as JSON data
    filtered_items = get_filtered_items_by_type(filter_type)
    
    return JsonResponse(filtered_items, safe=False)



import random
import string
from django.core.mail import send_mail
 
 

 
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.shortcuts import render

def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = get_random_string(length=6)  # Generate a random verification code
            
            try:
                user.profile.reset_code = reset_code
                user.profile.save()
            except:
                profile=Profile(user=user,reset_code=reset_code)
                profile.save()
            

            # Send the verification code via email
            send_mail(
                'Password Reset Verification Code',
                f'Your verification code is: {reset_code}',
                'joesdevil10@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('/verify_code/')
        except User.DoesNotExist:
            # Handle case where the email is not found
            return render(request, 'invalid_email.html')
    else:
        return render(request, 'enter_email.html')
    
    

def verify_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        reset_code = request.POST.get('reset_code')

        try:
            user = User.objects.get(email=email)
            if user.profile.reset_code == reset_code:
                return redirect(f'/change_password/{user.id}/')
            else:
                return render(request, 'invalid_code.html')
        except User.DoesNotExist:
            # Handle case where the email is not found
            return render(request, 'invalid_email.html')
    else:
        return render(request, 'verify_code.html')

 
 

from django.contrib.auth.hashers import make_password

def change_password(request, user_id):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = User.objects.get(pk=user_id)
        user.password = make_password(password)
        user.save()
        return render(request, 'password_changed.html')
    else:
        return render(request, 'change_password.html')
 

def payment_fail(request, cmd_id):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = User.objects.get(pk=user_id)
        user.password = make_password(password)
        user.save()
        return render(request, 'password_changed.html')
    else:
        return render(request, 'change_password.html')
 

def payement_succ(request, cmd_id):
    order= get_object_or_404(Order, id=int(cmd_id))
    if order.ref_code:
        confirmorderapi="https://test.satim.dz/payment/rest/confirmOrder.do?language=EN&orderId={}&password=satim120&userName=SAT2310130762".format(order.ref_code)
        orderidpai=requests.get(confirmorderapi)
        if orderidpai:
            if orderidpai.json()["depositAmount"] == order.get_total()*100:
                order.ordered = True
                order.approvalCode = orderidpai.json()["approvalCode"]
                order.depositAmount=orderidpai.json()["depositAmount"]/100
                order.message=orderidpai.json()["actionCodeDescription"]
                order.ip_address=orderidpai.json()["Ip"]
                order.cardholderName=orderidpai.json()["cardholderName"]
                order.paiement_meth="E"
                for item_ordered in order.items.all():
                    item_ordered.ordered = True
                    item_ordered.save() 
                order.save()
              
                send_mail(
                'Payement Status',
                f'Your Payement has been done , successfully! \n  with total of {order.get_total()} DZD.',
                'joesdevil10@gmail.com',
                [request.user.email],
                fail_silently=False,
                ) 

                try:
                    respCode_desc=orderidpai.json()["params"]["respCode_desc"]
                except:
                    respCode_desc=''
                
                OrderId=order.ref_code
                OrderNumber=order.id
                approvalCode=orderidpai.json()["approvalCode"]
                currency=""
                if orderidpai.json()["currency"] ==  "012":
                    currency="DZD"
                # date=orderidpai.json()["params"]["udf1"]
                date=order.modified_at
                mode_pai="CIB/Edhahabia"
                amount=orderidpai.json()["depositAmount"]/100;
                cardholder=orderidpai.json()["cardholderName"]
                context={
                    "mode_pai":mode_pai,
                    "date":date,
                    "currency":currency,
                    "approvalCode":approvalCode,
                    "OrderNumber":OrderNumber,
                    "OrderNumber":OrderNumber,
                    "OrderId":OrderId,
                    "amount":amount,
                    "cardholder":cardholder
                }






                return render(request, 'pay_succ.html',{'respCode_desc':respCode_desc,"context":context})
            else:
                order.paiement_meth="C"
                try:
                    rspcode=orderidpai.json()["params"]["respCode_desc"]
                except:
                    rspcode=''
                send_mail(
                'Payement Status',
                f'Your Payement has been rejected, please try to remove your ordered items and try again! , {rspcode}' ,
                'joesdevil10@gmail.com',
                [request.user.email],
                fail_silently=False,
                ) 
                respCode_desc =''
                action=''
                if orderidpai.json()["actionCodeDescription"] and orderidpai.json()["params"]=={}:
                    action=orderidpai.json()["actionCodeDescription"]
                

                try:
                    respCode1=orderidpai.json()["params"]["respCode"]
                except:
                    respCode1="00"

                    

                if  respCode1== "00" and int(orderidpai.json()["ErrorCode"]) ==  0  and int(orderidpai.json()["OrderStatus"]) == 3 :
                    respCode_desc ="Votre transaction a été rejetée"
                else:
                    try:
                        respCode_desc=orderidpai.json()["params"]["respCode_desc"]
                    except:
                        respCode_desc=''

                


                
                return render(request, 'payement_fail.html',{'respCode_desc':respCode_desc,'action':action})
        else:
            order.paiement_meth="C"
            order.save()
            return redirect("/")
    
    
 
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


def render_to_pdf(template_src, context_dict):

    # Load the template
    template = get_template('pdfDownload.html')  # Replace with the actual template name
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def generate_pdf(request, cmd_id):
    # Get data from your context (replace this with your actual data)
    tar_order= get_object_or_404(Order, id=int(cmd_id))
    
    
    
    context_data = {
        'respCode_desc': 'Payment Successful',
        'context': {
            'OrderId': tar_order.ref_code,
            'cardholder': tar_order.cardholderName,
            'OrderNumber': tar_order.id,
            'approvalCode':  tar_order.approvalCode,
            'date': tar_order.ordered_date,
            'amount': tar_order.depositAmount,
            'currency': "DZD"
        }
    }

    return render_to_pdf('pdfDownload.html', context_data)

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
def send_email_paiement(request,cmd_id):
    tar_order= get_object_or_404(Order, id=int(cmd_id))
    try:
        if request.user.email == tar_order.email:
            emails=[request.user.email]
        else:
            emails=[request.user.email,tar_order.email]
    except:
        emails=[request.user.email]

    if tar_order.approvalCode :
        approvalCode=tar_order.approvalCode
    else:
        approvalCode=""
    context_data = {
        'respCode_desc': 'Payment Successful',
        'context': {
            'cardholder': tar_order.cardholderName,
            'OrderId': tar_order.ref_code,
            'OrderNumber': tar_order.id,
            'approvalCode':  approvalCode,
            'date': tar_order.ordered_date,
            'amount': tar_order.depositAmount,
            'currency': "DZD"
        }
    }

    # send_mail(
    #             'Payement Status',
    #             f'Your Payement has been rejected, please try to remove your ordered items and try again! ' ,
    #             'joesdevil10@gmail.com',
    #             [request.user.email],
    #             fail_silently=False,
    #             ) 
    
    html_content = render_to_string('pdfDownload.html', context_data)

    # Create a unique filename based on the current date and time
    file_name =  "payement_status.pdf"

    # Create a BytesIO buffer to store the PDF content
    pdf_buffer = BytesIO()

    # Use xhtml2pdf to convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

    if pisa_status.err:
        # Handle the error, e.g., return a response with an error message
        return HttpResponse("Error generating PDF", status=500)

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    # Create an EmailMessage object
    email = EmailMessage(
        'Payement Status - Matacor',
        f'Your Payement has been done , successfully! \n  with total of {tar_order.get_total()} DZD.',
       'joesdevil10@gmail.com',
        emails,
    )

    # Attach the PDF file to the email
    email.attach(file_name, pdf_buffer.read(), 'application/pdf')
    
    email.send(fail_silently=False)

  
    

    return redirect("/")

