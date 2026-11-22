from django.urls import path
from . import views
from . import api_views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('api/', api_views.product_list_api, name='api_list'),
    path('home/', views.product_list_view, name='product_home'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('<int:pk>/', views.product_detail_view, name='detail'),
]
