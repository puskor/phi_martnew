from rest_framework import serializers
from order.models import Cart,CartItem,Order,OrderItem
from product.serializers import ProductSerializer
from product.models import Product
from .service import OrderService

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ["id","name","price"]

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta : 
        model = CartItem
        fields = ["id","product_id","quantity"]
        
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        try:
            cart_item = CartItem.objects.get(cart_id =cart_id,product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
            
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"{value} this product not in list")
        return value
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]
        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_item_price")
    class Meta:
        model = CartItem
        fields = ["id","cart","product","quantity","total_price"] 
        
    def get_total_item_price(self,cart_item :CartItem):
        return cart_item.quantity * cart_item.product.price
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_cart_price")
    class Meta:
        model = Cart
        fields = ["id","user","items","total_price"]
        read_only_fields = ["user"]
    def get_total_cart_price(self,cart:Cart):
        list = sum([item.product.price * item.quantity for item in cart.items.all()])
        return list
        

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id","product","quantity","price","total_price"]

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
        
    def update(self,instance,validated_data):
        user = self.context["user"]
        new_status = validated_data["status"]
        
        if new_status ==Order.CANCELED:
            return OrderService.order_canceled(order=instance,user=user)
        
        if not user.is_staff:
            raise serializers.ValidationError("you are not admin")
        
        # instance.status = new_status
        # instance.save()
        # return instance
        return super().update(instance,validated_data)
        
        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order
        fields = ["id","user","status","total_price","created_at","items"]

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField() 
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        return cart_id
    
        
        
    def create(self, validated_data):
        user_id = self.context["user_id"]
        cart_id = validated_data["cart_id"]
        try:
            order = OrderService.create_order(user_id=user_id,cart_id=cart_id)
            return order
        except ValueError as e:
            return serializers.ValidationError(str(e))
        
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data

