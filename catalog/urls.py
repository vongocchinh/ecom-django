# from django.urls import path
# # from . import views


# # urlpatterns = [
# #     path('',views.home,name='home')
# # ]

from django.urls import path
from .import views
urlpatterns = [
    path ('', views.HomeView.as_view(), name = 'index'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single-from-cart/<slug>',views.remove_single_from_cart,name='remove_single_from_cart'),
    path ('', views.HomeView.as_view(), name = 'home'),
    path ('product/<slug>', views.ProductDetail, name = 'product'),
    path('OrderSummaryView/',views.OrderSummaryView.as_view(),name='order_summary'),
    path('remove-from-cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path ('addProductReview/<slug>', views.addProductReview, name = 'addProductReview'),
    path('add_productReview_success/<slug>',views.ProductDetail,name='add_productReview_success'),
    path('checkout_success/',views.checkout_success,name='checkout_success'),
    path('brand_search/<name>',views.Brand_search,name='brand_search')
]