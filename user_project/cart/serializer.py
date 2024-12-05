from abc import ABC

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Cart


class AddToCartSerializer(ModelSerializer):
    id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['id', 'book_id', 'quantity']


class GetCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total_price = serializers.IntegerField()


class UpdateCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = '__all__'
