from rest_framework import generics, permissions

from .models import ProductModel
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        return ProductModel.objects.all()
