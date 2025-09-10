from . import views
from django.urls import path
urlpatterns = [
    path('',views.products, name='products'),
    path('add/',views.products_add, name='products_add'),
]
