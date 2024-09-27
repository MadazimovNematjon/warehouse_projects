import uuid
from dataclasses import field

from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from shared.models import BaseModel


class ProductModel(BaseModel):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=6, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['product_code'], name='unique_product_code'
            )
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name


class MaterialModel(BaseModel):
    material_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.material_name


class ProductMaterialModel(BaseModel):
    product_id = models.ForeignKey(ProductModel, related_name='product_materials', on_delete=models.CASCADE)
    material_id = models.ForeignKey(MaterialModel, related_name='materials_product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Product Material"
        verbose_name_plural = "Product Materials"

    def __str__(self):
        return f"{self.quantity} of {self.material_id.material_name} for {self.product_id.product_name}"

    @staticmethod
    def material_quantity(material_id):
        # data filtering
        product_material = ProductMaterialModel.objects.filter(material_id=material_id)

        quantity = 0
        # get data db
        if product_material.exists():
            # get the sum of all quantities belonging to the material id
            for pm in product_material:
                quantity += pm.quantity

        return quantity

    def validate_quantity(self, quantity):
        """Validate the quantity against available warehouse stock."""

        total_quantity = self.material_quantity(self.material_id)
        warehouses = WarehouseModel.objects.filter(material_id=self.material_id)

        if not warehouses.exists():
            print("No warehouses found for this material.")
            return False  # No warehouses available

        for warehouse in warehouses:
            available_quantity = warehouse.remainder - total_quantity
            if available_quantity >= quantity:
                self.save()

        raise ValidationError({
            "quantity": quantity,
        })

    def clean(self):
        """Perform custom validation before saving."""
        if not self.validate_quantity(self.quantity):
            raise ValidationError({
                'warehouse_id': None,
                'price': None,
                'detail': "Insufficient stock in warehouses."
            })

    def save(self, *args, **kwargs):
        """Override save to include validation."""
        try:
            self.clean()
            super().save(*args, **kwargs)  # Save only if validation passes
        except ValidationError as e:
            print(f"Validation error: {e}")
            return Response({"detail": "Saved successfully."}, status=HTTP_400_BAD_REQUEST)


class WarehouseModel(BaseModel):
    id = models.AutoField(primary_key=True, unique=True, editable=False, )
    material_id = models.ForeignKey(MaterialModel, related_name='warehouses', on_delete=models.CASCADE)
    remainder = models.PositiveIntegerField()  # Omborda qolgan miqdor
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return f"{self.remainder} left of {self.material_id.material_name} at {self.price} per unit"
