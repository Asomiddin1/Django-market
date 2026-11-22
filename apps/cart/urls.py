from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='detail'),
    path('add/<int:product_id>/', views.cart_add_view, name='add'),
    path('decrement/<int:product_id>/', views.cart_decrement_view, name='decrement'),
    path('remove/<int:product_id>/', views.cart_remove_view, name='remove'),
    path('clear/', views.cart_clear_view, name='clear'),
]
