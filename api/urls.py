from django.urls import path,include
# from rest_framework.routers import SimpleRouter,DefaultRouter
from product.views import ProductViewSets,CategoryViewSets,ReviewViewSets
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("product",ProductViewSets)
router.register("category",CategoryViewSets)

product_router = routers.NestedDefaultRouter(router,"product",lookup = "product")
product_router.register("review",ReviewViewSets,basename="product-review")


# urlpatterns = router.urls


urlpatterns = [
    path("",include(router.urls)),
    path("",include(product_router.urls))
    # path("product/",include("product.product_urls")),
    # path("category/",include("product.category_urls"))
    
]
