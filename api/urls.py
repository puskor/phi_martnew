from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from product.views import ProductViewSets,CategoryViewSets

router = DefaultRouter()
router.register("product",ProductViewSets)
router.register("category",CategoryViewSets)

# urlpatterns = router.urls


urlpatterns = [
    path("",include(router.urls))
    # path("product/",include("product.product_urls")),
    # path("category/",include("product.category_urls"))
    
]
