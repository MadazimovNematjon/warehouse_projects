from django.urls import path

from .views import ProductListView, MaterialListView, WarehouseListView, WarehouseCreateView, MaterialCreateView, \
    ProductCreateView, ProductMaterialCreateView, ProductMaterialListView

urlpatterns = [
    path('product/', ProductListView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product-material/create/', ProductMaterialCreateView.as_view()),
    path('product-material/list/', ProductMaterialListView.as_view()),

    path('material/', MaterialListView.as_view()),
    path('material/create', MaterialCreateView.as_view()),
    path('warehouse/', WarehouseListView.as_view()),
    path('warehouse/create', WarehouseCreateView.as_view())

]
