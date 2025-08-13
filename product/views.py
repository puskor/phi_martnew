from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from product.models import Product,Category
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.
@api_view(["GET","POST"])
def view_products(request):
    if request.method == "GET":
        product=Product.objects.select_related().all()
        serializer = ProductSerializer(product,many = True,context={'request': request})
        return Response(serializer.data)
    if request.method == "POST":
        serializer = ProductSerializer(data = request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewProduct(APIView):
    def get(self , request):
        product = Product.objects.select_related().all()
        serializer = ProductSerializer(product,many=True,context ={'request':request})
        return Response(serializer.data)
    def post(self,request):
        serializer = ProductSerializer(data = request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    
class ProductList(ListCreateAPIView):
    # queryset  = Product.objects.select_related().all()
    # serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.select_related().all()
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {"request":self.request}
    
class ProductViewSets(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def destroy(self,request ,*args, **kwargs):
        product = self.get_object()
        if product.stock >10:
            return Response({"massage" : "You can not delete stock more than 10"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view(["GET","PUT","DELETE"])
def view_one_products(request,pk):
    if request.method =="GET":
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    if request.method == "PUT":
        product =get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,data =request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == "DELETE":
        product = get_object_or_404(Product,pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class ViewOneProduct(APIView):
    def get(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    def put(self,request,pk):
        product= get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,data =request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,pk): 
        product = get_object_or_404(Product,pk=pk)
        copy_list = product
        product.delete()
        serializer = ProductSerializer(copy_list,context={'request': request})
        return Response(serializer.data ,status=status.HTTP_204_NO_CONTENT)
    
class ProductDetailsList(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def delete(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        if product.stock >10:
            return Response({"message" : "Stock more than 10 so not be delete"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        


@api_view(["GET","POST"])
def view_category(request):
    if request.method =="GET":
        category = Category.objects.select_related().annotate(product_count = Count("products")).all()
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # print("2nd")
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        # else :
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ViewCategory(APIView):
    def get(self,request):
        category = Category.objects.select_related().annotate(product_count = Count("products")).all()
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data)
    def post(self,request):
        # category = Category.objects.select_related().all()
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class CategoryList(ListCreateAPIView):
    queryset = Category.objects.select_related().annotate(product_count = Count("products")).all()
    # queryset = Category.objects.select_related().all()
    serializer_class =CategorySerializer
    
    # def get_queryset(self):
    #     return Category.objects.select_related().annotate(product_count = Count("products")).all()
    # def get_serializer_class(self):
    #     return CategorySerializer


@api_view()
def view_one_category(request,pk):
    category = Category.objects.get(pk=pk)
    category_dic = {"id":category.pk ,"name":category.name }
    return Response(category_dic)

class ViewOneCategory(APIView):
    def get(self,request,pk):
        category = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    def put(self,request,pk):
        category = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    def delete(self,request,pk):
        category = get_object_or_404(Category,pk=pk)
        copy_c = category
        category.delete()
        serializer = CategorySerializer(copy_c)
        return Response(serializer.data , status=status.HTTP_204_NO_CONTENT)
    
class CategoryDetailsList(RetrieveUpdateDestroyAPIView):
    queryset  = Category.objects.all()
    serializer_class = CategorySerializer
