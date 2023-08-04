from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('api/product/', views.ProductListApiView.as_view(), name='product_api_list'),
]
