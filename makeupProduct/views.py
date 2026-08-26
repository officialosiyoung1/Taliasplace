from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import cloudinary
import cloudinary.uploader

from .models import MakeupProduct
from .serializers import MakeupProductSerializer

cloudinary.config(
    cloud_name='sq9jwods',
    api_key='155885138724686',
    api_secret='TBg7M6HFC0G1VJVIPa-bahtMzsw',
    secure=True,
)


class MakeupProductGetAllView(generics.ListAPIView):
    queryset = MakeupProduct.objects.all().order_by('-id')
    serializer_class = MakeupProductSerializer
    permission_classes = [permissions.AllowAny]


class MakeupProductCreateView(generics.CreateAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'image' in request.FILES:
            image_file = request.FILES['image']
            try:
                upload_result = cloudinary.uploader.upload(image_file)
                data['image'] = upload_result.get('secure_url', '')
            except Exception as exc:
                return Response(
                    {"error": "Image upload failed", "details": str(exc)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MakeupProductUpdateView(generics.UpdateAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != request.user:
            return Response(
                {"error": "You do not have permission to update this product"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeupProductDeleteView(generics.DestroyAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this product"},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(instance)
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)


class MakeupProductDetailView(generics.RetrieveAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [permissions.AllowAny]


class MakeupProductSingleView(generics.RetrieveAPIView):
    queryset = MakeupProduct.objects.all()
    serializer_class = MakeupProductSerializer
    permission_classes = [permissions.AllowAny]


