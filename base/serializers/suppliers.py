from rest_framework import serializers

from base.models.supplier import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'supplier_name',
            'phone_number_1',
            'phone_number_2',
            'email',
            'physical_address',
            'pin_number',
            'vat_number',
            'contact_person',
        ]
