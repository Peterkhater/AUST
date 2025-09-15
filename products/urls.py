from . import views
from django.urls import path
urlpatterns = [
    path('',views.products, name='products'),
    path('add/',views.products_add, name='products_add'),
    path('view/<int:id>',views.products_view, name='products_view'),
    path('delete/<int:id>',views.product_delete, name='products_delete'),
    path('product_edit/<int:product_id>',views.edit_product, name='products_edit'),
    # path('statistic',views.market_statistics_view, name='products_stat'),
]
