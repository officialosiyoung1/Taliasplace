from rest_framework import serializers
from .models import MakeupProduct


class MakeupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeupProduct
        fields = ['id', 'name', 'brand', 'quantity', 'colour', 'price', 'owner']
        read_only_fields = ['owner']

        def create(self, validated_data):
            return MakeupProduct.objects.create(**validated_data)
        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.brand = validated_data.get('brand', instance.brand)
            instance.quantity = validated_data.get('quantity', instance.quantity)
            instance.color = validated_data.get('color', instance.color)
            instance.price = validated_data.get('price', instance.price)
            instance.save()
            return instance
        
        