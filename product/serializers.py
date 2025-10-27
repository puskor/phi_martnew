from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review,ProductImage
from django.contrib.auth import get_user_model

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     description = serializers.CharField()
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ["id","name","description","product_count"]
    product_count = serializers.IntegerField(read_only = True)
        

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     Unit_price = serializers.DecimalField(max_digits=10,decimal_places=3,source="price")
#     tax_with_price = serializers.SerializerMethodField(method_name="calculate_tax")
#     # category = serializers.PrimaryKeyRelatedField(queryset= Category.objects.all())
#     # category =serializers.StringRelatedField() 
#     # categoryy = CategorySerializer(source = "category")
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name = "category-one-list"
#     )
#     def calculate_tax(self,products):
#         return round(products.price * Decimal(1.1),3)

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model  = ProductImage
        fields = ["id","image"]
    
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True , read_only =True)
    class Meta:
        model = Product
        fields = ["id","name","price","description","stock","price_with_tax","category","images"]
        
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name = "category-detail"
        )
        
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1),2)
    
    def validate_price(self,price):
        if price < 0:
            raise serializers.ValidationError("Price must be positive and price>0")
        return price
    
    def validate_stock(self,stock):
        if stock < 0 :
            raise serializers.ValidationError("Stock must be positive")
        return stock
    
class SimpleUserSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField(
        method_name= "current_user_name"
    )
    class Meta:
        model = get_user_model()
        fields = ["id","name"]
    
    def current_user_name(self,obj): 
        return obj.get_full_name()
        
        
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(
        method_name= "get_user"
    )
    class Meta:
        model = Review
        fields = ["id","product","user","review","comment","create_at","update_at"]
        read_only_fields = ["user","product"]
        
    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data
        
    def create(self, validated_data):
        product_id = self.context["product_pk"]
        return Review.objects.create(product_id = product_id,**validated_data)
    
    
