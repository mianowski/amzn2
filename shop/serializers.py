from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'name', 'price_in_dollars', 'barcode', 'description')


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Order.objects.all(), source='order.id')

    class Meta:
        model = models.OrderItem
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        # fields = ('id', 'items', 'start_date', 'ordered_date', 'ordered')
