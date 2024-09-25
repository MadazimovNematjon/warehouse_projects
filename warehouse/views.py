from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProductModel, WarehouseModel, MaterialModel, ProductMaterialModel
from .serializers import ProductSerializer, WarehouseSerializer, MaterialSerializer, ProductMaterialSerializer


# Product
class ProductListView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        try:
            product = ProductModel.objects.all()
            serializer = ProductSerializer(product, many=True)

            if serializer.data:
                data = {
                    'success': True,
                    'result': serializer.data,
                    'message': 'Successfully fetched products'
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {'success': False, 'error': str(e), 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        request_body=ProductSerializer(write_only=('product_id', 'material_id', 'quantity')),

    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {'success': False, 'error': str(e), 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# MaterialProduct
class ProductMaterialListView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        try:
            mp = ProductMaterialModel.objects.all()
            serializer = ProductMaterialSerializer(mp, many=True)
            if serializer.data:
                data = {
                    'success': True,
                    'data': serializer.data,
                    'message': 'Successfully fetched material products'
                }
                return Response(data, status=status.HTTP_200_OK)
            data = {'success': False, 'error': serializer.errors, 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {'success': False, 'error': str(e), 'message': 'Something went wrong'}

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProductMaterialCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        request_body=ProductMaterialSerializer,
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = ProductMaterialSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'success': True, 'result': serializer.data, 'message': 'Successfully create material products'}
                return Response(data, status=status.HTTP_201_CREATED)
            data = {'success': False, 'error': serializer.errors, 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# Material
class MaterialListView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    queryset = MaterialModel.objects.all()


class MaterialCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        request_body=MaterialSerializer,
        responses={205: 'Successful', 400: 'Bad Request'},

    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = MaterialSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'success': True, 'result': serializer.data, 'message': 'Successfully created'}
                return Response(data, status=status.HTTP_201_CREATED)
            data = {'success': False, 'error': serializer.errors, 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# WareHouse
class WarehouseListView(generics.ListAPIView):
    serializer_class = WarehouseSerializer
    queryset = WarehouseModel.objects.all()
    permission_classes = [permissions.AllowAny, ]


class WarehouseCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        request_body=WarehouseSerializer,
        responses={205: 'Successful', 400: 'Bad Request'},
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = WarehouseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'success': True, 'result': serializer.data, 'message': 'Successfully created'}
                return Response(data, status=status.HTTP_201_CREATED)
            data = {'success': False, 'error': serializer.errors, 'message': 'Something went wrong'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
