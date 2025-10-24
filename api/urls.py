from django.urls import path,include
# from rest_framework.routers import SimpleRouter,DefaultRouter
from product.views import ProductViewSets,CategoryViewSets,ReviewViewSets,ProductImageViewSets
from order.views import CartViewSet,CartItemViewset,OrderViewset
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("product",ProductViewSets,basename="product")
router.register("category",CategoryViewSets)
router.register("cart",CartViewSet,basename="cart")
router.register("order",OrderViewset,basename="order")


product_router = routers.NestedDefaultRouter(router,"product",lookup = "product")
product_router.register("review",ReviewViewSets,basename="product-review")
product_router.register("images",ProductImageViewSets,basename="product-image")

cart_router = routers.NestedDefaultRouter(router,"cart",lookup = "cart")
cart_router.register("items",CartItemViewset,basename="cart-item")

# urlpatterns = router.urls


urlpatterns = [
    path("",include(router.urls)),
    path("",include(product_router.urls)),
    path("",include(cart_router.urls)),
    path("auth/",include('djoser.urls.jwt')),
    path("auth/",include('djoser.urls')),
    
    
    # path("product/",include("product.product_urls")),
    # path("category/",include("product.category_urls"))
    
]
