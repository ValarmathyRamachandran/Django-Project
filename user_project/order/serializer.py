from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Order


class OrderCheckOutSerializer(ModelSerializer):
    address = serializers.CharField(max_length=300)

    class Meta:
        model = Order
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
