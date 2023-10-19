from rest_framework import serializers

from mainapp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
