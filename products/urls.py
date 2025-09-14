from . import views
from django.urls import path
urlpatterns = [
    path('',views.products, name='products'),
    path('add/',views.products_add, name='products_add'),
    path('view/<int:id>',views.products_view, name='products_view'),
    # path('statistic',views.market_statistics_view, name='products_stat'),
]
