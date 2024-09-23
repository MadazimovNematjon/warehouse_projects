from django.urls import path

from .views import ProductAPIView,ProductMaterialAPIView,WarehouseAPIView,MaterialAPIView,ProductListView

urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('warehouse/', WarehouseAPIView.as_view()),
    path('product/', ProductAPIView.as_view()),
    path('material/', MaterialAPIView.as_view()),
    path('product-material/', ProductMaterialAPIView.as_view()),

]
