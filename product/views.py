from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from product.models import Product,Category,Review,ProductImage
from product.serializers import ProductSerializer,CategorySerializer,ProductImageSerializer
from product import serializers
from django.db.models import Count
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFiler
from rest_framework.filters import SearchFilter,OrderingFilter
from product.paginations import DefaultPagination
# from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from .permissions import IsReviewerOrReadOnly

class ProductViewSets(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ["category_id","price"]
    filterset_class = ProductFiler
    search_fields = ["name","description"]
    ordering_fields = ["price"]
    pagination_class = DefaultPagination
    # permission_classes = [IsAdminOrReadOnly]    
    # permission_classes = [DjangoModelPermissions]
    permission_classes  = [DjangoModelPermissionsOrAnonReadOnly]
    
    
    
    
    # def get_permissions(self):
    #     if self.request.method =='GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get("category_id")
    #     if category_id is not None:
    #         print("b")
    #         queryset = Product.objects.filter(category_id = category_id)
    #     return queryset
    
    
    def destroy(self,request ,*args, **kwargs):
        product = self.get_object()
        if product.stock >10:
            return Response({"massage" : "You can not delete stock more than 10"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductImageViewSets(ModelViewSet):
    
    serializer_class = ProductImageSerializer
    # permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs.get("product_pk"))
    def perform_create(self, serializer):
        serializer.save(product_id = self.kwargs.get("product_pk"))


class CategoryViewSets(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [DjangoModelPermissions]
    


class ReviewViewSets(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class= serializers.ReviewSerializer
    permission_classes  = [IsReviewerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs.get("product_pk"))
    
    # 
    def get_serializer_context(self):
        context = super().get_serializer_context
        if getattr(self, 'swagger_fake_view', False):
            return context
        return {"product_pk" : self.kwargs.get("product_pk")}