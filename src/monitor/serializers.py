from rest_framework import serializers
from .models import Product, ProductsPrices

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'price', 'start_date', 'end_date']


class ProductResponseSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'price', 'start_date', 'end_date']


class ProductsPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsPrices
        fields = ('price', 'start_date', 'end_date')


class CalculateAveragePriceSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class LatestPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsPrices
        fields = ['price']

class ProductWithLatestPriceSerializer(serializers.ModelSerializer):
    latest_price = LatestPriceSerializer(source='get_latest_price', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'latest_price']