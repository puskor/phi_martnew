from django.urls import path
from product import views

urlpatterns = [
    path("",views.ProductList.as_view() ,name="products-list"),
    path("<int:pk>/",views.ProductDetailsList.as_view() ,name="product-one-list"),
    
]
