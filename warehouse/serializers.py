from rest_framework import serializers

from warehouse.models import ProductModel, MaterialModel, ProductMaterialModel, WarehouseModel


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = [
            'material_name', 'material_id', 'created_at', 'updated_at'
        ]


class ProductMaterialSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.SerializerMethodField('get_warehouse_id')
    material_name = serializers.CharField(source='material_id.material_name')
    qty = serializers.IntegerField(source='quantity')
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = ProductMaterialModel
        fields = [
            'warehouse_id',
            'product_id',
            'material_id',
            'quantity',
            'material_name',
            'qty',
            'price',
            'created_at',
            'updated_at',
        ]

        extra_kwargs = {
            'warehouse_id': {'required': False, 'read_only': True},
            'material_name': {'required': False, 'read_only': True},
            'price': {'required': False, 'read_only': True},
        }

    # Get the warehouse_id based on the material

    @staticmethod
    def get_warehouse_id(obj):
        warehouse = WarehouseModel.objects.filter(material_id=obj.material_id).first()
        return warehouse.id if warehouse else None

    # Get the price based on the material

    @staticmethod
    def get_price(obj):
        price = WarehouseModel.objects.filter(material_id=obj.material_id).first()
        return price.price if price else None


class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True, source='material_id')

    class Meta:
        model = WarehouseModel
        fields = [
            'id', 'material_id', 'remainder', 'price', 'material', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'material': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, )
    product_qty = serializers.SerializerMethodField('get_product_qty')

    class Meta:
        model = ProductModel
        fields = [
            'product_name',
            'product_qty',
            'product_materials',
            'created_at',
            'updated_at'
        ]

    @staticmethod
    def get_product_qty(obj):
        return obj.product_materials.count()
