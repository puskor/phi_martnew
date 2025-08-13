from django.urls import path,include
from rest_framework.routers import SimpleRouter
from product.views import ProductViewSets

router = SimpleRouter()

router.register("product",ProductViewSets)

urlpatterns = [
    path("product/",include("product.product_urls")),
    path("category/",include("product.category_urls"))
    
]
