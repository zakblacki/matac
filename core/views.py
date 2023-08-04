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

from django.contrib.auth.forms import UserCreationForm
stripe.api_key = settings.STRIPE_SECRET_KEY

from django import template

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
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user is not None:
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')  # Redirect to the home page after successful login
            # Add an error message here if login fails
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
            user_wish = WishList.objects.filter(user=request.user)
            if user_wish.first():
                user_wish =user_wish.first()
                if item in user_wish.items.all():
                    
                    user_wish.items.remove(item)
                else:
                    user_wish.items.add(item)
                    
                 
            else:
                WishList.objects.create(
                    user= request.user,
                     
                )
                WishList.objects.get(
                    user= request.user,
                ).items.add(item)
             
                
        else:
            return redirect("wishlist")
        
        return redirect(f"/product/{slug}/")
    else:
        return redirect("/login")
     

def logout_view(request):
    logout(request)
    return redirect('/')

def wishlist_view(request):
     
    
 
    
    context={}
    try:
        if request.user.is_authenticated:
            
            user_wish=WishList.objects.filter(user=request.user).first()
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
    
    context={
        "items":Item.objects.filter(is_active=True),
        "category":Category.objects.filter(is_active=True),
        "new_items":Item.objects.filter(label="N"),
        "most_sale":Item.objects.filter(label="S"),
        "essentials":Essential.objects.filter(is_active=True),
        
    }

    return render(request, 'index.html',context) 


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        
        if len(OrderItem.objects.filter(user=self.request.user, ordered=False)) !=0:
            try:
                order = OrderItem.objects.filter(user=self.request.user, ordered=False)
                
                context = {
                    'object': order,
                    "form":FormInput()
                }
                return render(self.request, 'order_summary.html', context)
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order")
                return redirect("/")
        else:
            return redirect("/")

    def post(self, *args, **kwargs):
        form = FormInput(self.request.POST,self.request.FILES)
        
        print("posts  none")
        if form.is_valid():
            
        
            phone=form.cleaned_data.get("phone") 
            email=form.cleaned_data.get("email")
            address=form.cleaned_data.get("address")
            fullname=form.cleaned_data.get("fullname")
            
            
           
        
            order = Order.objects.get(user=self.request.user, ordered=False)
         
            amount = int(order.get_total() * 100)
            try:
                
                
                order.ref_code = create_ref_code()
                order.ordered = True
                    
                    
                for item_ordered in order.items.all():
                    item_ordered.ordered = True
                    item_ordered.save()   
                
                order.total_amount=order.get_total()
                order.phone_number=phone
                order.shipping_address = address
                if form.cleaned_data.get("recu_img"):
                    img=form.cleaned_data.get("recu_img")
                    order.recui_image = img
                
                
                order.save()

                

                messages.success(self.request, "Order was successful")
                return redirect("/confirm_order/{}/{}/".format(self.request.user,order.id))

        
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.error(self.request, "Something went wrong")
                return redirect("/")

            except  :
                # send an email to ourselves
                messages.error(self.request, "Serious Error occured")
        return redirect("/")

class ShopView(ListView):
    model = Item
    paginate_by = 9
    template_name = "shop.html"
    
    def get(self, *args, **kwargs):  
        filtermeth=""  
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
                            
                            if get_val != "" :
                                print(get_val)
                                query_srch |= Q(title__icontains=get_val)
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
                            
                    
                if query_srch :
                    
                    comb_final = query_srch & combined_query & combined_query5 & combined_query3
                else:
                    comb_final = combined_query & combined_query5 & combined_query3
                item= Item.objects.filter(comb_final,is_active=True)

                if filtermeth:
                     
                    
                    item =Item.objects.filter(comb_final,is_active=True).order_by(filtermeth)
                else:
                    pass
            else:
                item = Item.objects.filter( is_active=True)
                 

        except:
            item = Item.objects.filter( is_active=True)
        context = {
            'object_list': item,
             
             
        }
        return render(self.request, "shop.html", context)             



@login_required
def profile(request):
    context={}
    
    ordered= Order.objects.filter(user=request.user)
    context["orders"]=ordered
    
    return render(request,"profile.html",context)

@login_required
def confirmorder(request,slug,slug1):
    context={}
    print(slug,request.user)
    
    ordertar= None
    context={}
    
    if str(slug.replace(" ","")) == str(request.user):
        print("yesss user")
        ordertar=get_object_or_404(Order, id=int(slug1))
        print(ordertar)
        context["target"]=ordertar
        
    if request.method == "POST":
         
        context["form"]=UploadImg(request.POST,request.FILES)
        if context["form"].is_valid():
            
             
            
             
            ordertar.recui_image = request.FILES.get("recu_img")
            ordertar.save()
            print(request.FILES.get("recu_img"))
            # ordertar.recui_image = img
            # ordertar.save()
    else:
        context["form"]=UploadImg()
     
    
    return render(request,"confirm_order.html",context)


class ItemDetailView(DetailView):
    model = Item

    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # Add additional data to the context
        context['images'] =ImageItem.objects.filter(slug=self.object.slug) 
        context["details"] =  self.object.details 
        
        print(self.object.details)
        context["colors_item"] = Item.objects.filter(article_id=self.object.article_id)
        
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


             
            
         
        else:
            context["relate_pros"] =  Item.objects.filter(category=self.object.category).exclude(pk=self.object.pk) 

           
         
        
        # Get all comments related to the post
        return context

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        combined_query = Q()
        filtermeth=""
        bannertarg=[]
        banners=[]
        # print(category)
        for cattg in TopCategory.objects.filter(items__title=category):
            if len(Banner_category.objects.filter(category__title=cattg.title))>0:
                if category in cattg.items.all():
                    
                    for itmc in Banner_category.objects.filter(category__title=cattg.title):
                        banners.append(itmc)
                    print(banners)
                # bannertarg=Banner_category.objects.filter(category__title=cattg.title)
                # print(bannertarg )
                # banners=bannertarg
                # print(cattg.title)
            # for catt in TopCategory.objects.filter(items__title=category):
                
            #     print(Banner_category.objects.filter(category__title=catt.title))
                
           
                
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
                        if combined_query1 and combined_query2:
                            combined_query3 |=combined_query1 & combined_query2
                            
                
                        
                combined_cat = Q(category__exact=category)
                comb_final =combined_cat & combined_query & combined_query5 & combined_query3
                item= Item.objects.filter(comb_final,is_active=True)
                if filtermeth:
                     
                    
                    item =Item.objects.filter(comb_final,is_active=True).order_by(filtermeth)
                else:
                    pass
            else:
                item = Item.objects.filter(category=category, is_active=True)
                 

        except:
            item = Item.objects.filter(category=category, is_active=True)
             
       
            
         
         
        
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image.url,
             'banners':banners
        }
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
            
            print("success")
        
            order = Order.objects.get(user=self.request.user, ordered=False)
         
            amount = int(order.get_total() * 100)
            try:
                
                
                order.ref_code = create_ref_code()
                order.ordered = True
                    
                    
                for item_ordered in order.items.all():
                    item_ordered.ordered = True
                    item_ordered.save()   
                
                order.total_amount=order.get_total()
                order.phone_number=phone
                order.shipping_address = address
                order.recui_image = img
                
                
                order.save()

                

                messages.success(self.request, "Order was successful")
                return redirect("/")

        
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.error(self.request, "Something went wrong")
                return redirect("/")

            except  :
                # send an email to ourselves
                messages.error(self.request, "Serious Error occured")
        return redirect("/")



# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "index.html", context)
#
#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product-detail.html", context)
#
#
# def shop(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "shop.html", context)


@login_required
def add_to_cart(request, slug):
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
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
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
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Item was removed from your cart.")
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


@login_required
def remove_single_item_from_cart(request, slug):
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


