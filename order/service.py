from .models import Cart,CartItem,Order,OrderItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied,ValidationError
class OrderService:
    @staticmethod
    def create_order(user_id,cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk = cart_id)
            cart_item = cart.items.select_related("product").all()
            
            total_price = sum(item.product.price * item.quantity for item in cart_item)
            
            order = Order.objects.create(user_id=user_id,total_price=total_price)

            order_items =[
                OrderItem(
                    order = order,
                    product =  item.product,
                    price = item.product.price,
                    quantity = item.quantity,
                    total_price = item.product.price * item.quantity
                    
                    ) for item in cart_item
            ]

            OrderItem.objects.bulk_create(order_items)
            cart.delete()
            
            return order
    
    @staticmethod
    def order_canceled(order,user):
        if user.is_staff :
            order.status = Order.CANCELED
            order.save()
            return order
        if order.user != user :
            raise PermissionDenied("You can change only your cart")
        if order.status == Order.DELIVERED :
            raise ValidationError("You can not canceled this product")
        
        order.status = Order.CANCELED
        order.save()
        return order