from django.shortcuts import render
from .models import MakeupProduct 
from rest_framework import generics, permissions
from .serializers import MakeupProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class MakeupProductGetAllView(generics.ListAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        
    
class MakeupProductCreateView(generics.CreateAPIView):
    permissions_classes = [IsAuthenticated]
    print("PERMISSION CLASSES:", permissions_classes)
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        if self.request.method == 'post':
            return [permissions.IsAuthenticated()]
        
class MakeupProductUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = self.kwargs.get('pk')
        try:
            product = MakeupProduct.objects.get(pk=product_id)
        except MakeupProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if product.owner != self.request.user:
            return Response({"error": "You do not have permission to update this product"}, status=status.HTTP_403_FORBIDDEN) 
        product.name = serializer.validated_data.get('name', product.name)
        product.brand = serializer.validated_data.get('brand', product.brand)
        product.quantity = serializer.validated_data.get('quantity', product.quantity)
        product.colour = serializer.validated_data.get('colour', product.colour)
        product.price = serializer.validated_data.get('price', product.price)
        product.save()
        return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)  
        
        
class MakeupProductDeleteView(generics.DestroyAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
        if self.request.method == 'delete':
            return [permissions.IsAuthenticated()]
        try:
            instance.delete()
        except Exception as e:
            raise e
        
class MakeupProductDetailView(generics.ListAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

class MakeupProductSingleView(generics.RetrieveAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]
        

        

        
        



