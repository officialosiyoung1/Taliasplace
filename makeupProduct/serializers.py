from rest_framework import serializers

from .models import MakeupProduct


class MakeupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeupProduct
        fields = ['id', 'name', 'brand', 'quantity', 'colour', 'description', 'price', 'image', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        return MakeupProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
