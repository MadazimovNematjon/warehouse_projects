from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductModel, MaterialModel, ProductMaterialModel, WarehouseModel
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer




class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny,]

    def get_queryset(self):
        return ProductModel.objects.all()



# Product APIView
class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Material APIView
class MaterialAPIView(APIView):
    def get(self, request, *args, **kwargs):
        materials = MaterialModel.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ProductMaterial APIView
class ProductMaterialAPIView(APIView):
    def get(self, request, *args, **kwargs):
        product_materials = ProductMaterialModel.objects.all()
        serializer = ProductMaterialSerializer(product_materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        material_id = request.data.get('material_id')
        quantity = request.data.get('quantity')

        # Qo'shimcha validatsiya
        if quantity is None or int(quantity) <= 0:
            return Response({"error": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductMaterialSerializer(data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Warehouse APIView
class WarehouseAPIView(APIView):
    def get(self, request, *args, **kwargs):
        warehouses = WarehouseModel.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            # Narx validatsiyasi
            if serializer.validated_data['price'] <= 0:
                return Response({"error": "Price must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
