from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import *
from django.http import HttpResponseRedirect
import ast
from django.db.models import Q
from django.forms.models import model_to_dict


# Create your views here.
import random
import string
import stripe
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
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "u have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "RateLimitError")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not Authentication")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(self.request, "Serious Error occured")
            return redirect("/")


class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'

def index(request):
    context={
        "items":Item.objects.filter(is_active=True),
        "category":Category.objects.filter(is_active=True),
        "new_items":Item.objects.filter(label="N"),
        "most_sale":Item.objects.filter(label="S")
        
    }

    return render(request, 'index.html',context) 


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ShopView(ListView):
    model = Item
    paginate_by = 9
    template_name = "shop.html"
    def get(self, *args, **kwargs):    
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
                            
                        
                        if combined_query1 and combined_query2:
                            combined_query3 |=combined_query1 & combined_query2
                            
                    
                
                comb_final = combined_query & combined_query5 & combined_query3
                item= Item.objects.filter(comb_final,is_active=True)
             
            else:
                item = Item.objects.filter( is_active=True)
                 

        except:
            item = Item.objects.filter( is_active=True)
        context = {
            'object_list': item,
             
             
        }
        return render(self.request, "shop.html", context)             


class ItemDetailView(DetailView):
    model = Item

    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # Add additional data to the context
        context['images'] =ImageItem.objects.filter(slug=self.object.slug) 
        context["details"] = ast.literal_eval(self.object.details)
        context["colors_item"] = Item.objects.filter(article_id=self.object.article_id)

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
            context["relate_pros"] =  Item.objects.filter(category__icontains=self.object.category).exclude(pk=self.object.pk) 

           
         
        
        # Get all comments related to the post
        return context


# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        combined_query = Q()
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
                            
                        
                        if combined_query1 and combined_query2:
                            combined_query3 |=combined_query1 & combined_query2
                            
                    
                combined_cat = Q(category__exact=category)
                comb_final =combined_cat & combined_query & combined_query5 & combined_query3
                item= Item.objects.filter(comb_final,is_active=True)
             
            else:
                item = Item.objects.filter(category=category, is_active=True)
                 

        except:
            item = Item.objects.filter(category=category, is_active=True)
             
       
            
         
         
        
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image.url,
             
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
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
             
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


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
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
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
                ordered=False
            )[0]
            order.items.remove(order_item)
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
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
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


