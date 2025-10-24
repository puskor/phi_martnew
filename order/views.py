from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin 
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer,OrderItemSerializer,CreateOrderSerializer,UpdateOrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# Create your views here.


class CartViewSet(CreateModelMixin,GenericViewSet,DestroyModelMixin,RetrieveModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related("items__product").filter(user = self.request.user)



class CartItemViewset(ModelViewSet): 
    http_method_names = ["get","post","patch","delete"]
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id":self.kwargs.get("cart_pk")}
            
        
    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(cart_id = self.kwargs.get("cart_pk"))
    
class OrderViewset(ModelViewSet):
    # serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get","post","delete","patch"]
    
    def get_permissions(self):
        if self.request.method =="DELETE": 
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method =="PATCH":
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context
        return {"user_id":self.request.user.id , "user":self.request.user} 
    
    def get_queryset(self):
        if self.request.user.is_staff:  
            return Order.objects.all()
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.prefetch_related("items__product").filter(user = self.request.user)