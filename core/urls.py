from django.urls import path
from .views import (
    ItemDetailView,
    HomeView,
    add_to_cart,
    remove_from_cart,
    ShopView,
    OrderSummaryView,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    CategoryView,
    ItemListView
)
from .views import *

app_name = 'core'

urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('', index, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/ccp', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('items/', ItemListView.as_view(), name='item-retrieve-update-destroy'),
    path('login/', login_view, name='login_'),
    path('logout/', logout_view, name='logout_'),
    path('register/', register_view, name='register_'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist-add/<slug>/', wishlist_add_view, name='wishlist-add'),
]

handler404 = 'core.views.custom_page_not_found_view'
handler500 = 'core.views.custom_server_error_view'