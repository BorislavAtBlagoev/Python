from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from orders.models import Order, OrdersProducts


class OrdersProductsSerializer(ModelSerializer):
    price = serializers.ReadOnlyField(source='get_price')

    class Meta:
        model = OrdersProducts
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table', 'user', 'status', 'products', 'created_at', 'updated_at', 'created_by', 'updated_by']


class IsDeletedSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['is_deleted']
