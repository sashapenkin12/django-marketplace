from rest_framework import serializers
from rest_framework.fields import empty

from products.serializers import TagSerializer, ProductSerializer
from products.models import Product
from users.views import get_setting
from .models import Order

class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products that was added to orders.

    Attributes:
        tags: Tags serializer.
        reviews: Number of product reviews that defined by method.

    Methods:
        get_reviews: Get number of reviews on product instance.
        create: Add product to current order.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.

    """
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date',
                  'title', 'description', 'freeDelivery', 'tags',
                  'reviews', 'rating')

    def __init__(self, create_order=False, instance=None, data=empty, **kwargs):
        if create_order:
            self.order = Order.objects.create()
        super().__init__(instance, data, **kwargs)

    @classmethod
    def get_reviews(cls, instance):
        return instance.reviews.count()

    def create(self, validated_data) -> int:
        title, description = validated_data.get('title'), validated_data.get('description')
        product = Product.objects.get(title=title, description=description)
        product.count = validated_data.get('count')
        product.save()
        self.order.products.add(product)
        self.order.save()
        return self.order.id

    def delete_order(self):
        self.order.delete()


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.

    Attributes:
        createdAt: Order creation date.
        deliveryType: Type of the delivery.
        paymentType: Payment type.
        totalCost: Total cost of order's items.
        status: Order status.
        products: Order items.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.

    Methods:
        get_created_at: Get creation date as a string.
        get_delivery_type: Get delivery type as a string.
        get_payment_type: Get payment type as a string.
        get_total_cost: Get cost of order items.
        get_status: Get product status as a string.
    """
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    deliveryType = serializers.SerializerMethodField(method_name='get_delivery_type')
    paymentType = serializers.SerializerMethodField(method_name='get_payment_type')
    totalCost = serializers.SerializerMethodField(method_name='get_total_cost')
    status = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'createdAt', 'fullName', 'email',
            'phone', 'deliveryType', 'paymentType',
            'totalCost', 'status', 'city', 'address',
            'products'
        )

    @classmethod
    def get_created_at(cls, instance):
        return instance.date.strftime('%Y/%m/%d-%H:%M:%S')

    @classmethod
    def get_delivery_type(cls, instance):
        return 'ordinary' if instance.deliveryType == 0 else 'express'

    @classmethod
    def get_payment_type(cls, instance):
        return 'online' if instance.paymentType == 0 else 'Online with foreign account'

    @classmethod
    def get_total_cost(cls, instance):
        total_cost = 0
        for product in instance.products.all():
            total_cost += float(product.price * product.count)
        if instance.deliveryType == 1:
            total_cost += get_setting('express_delivery_price', default=5)
        else:

            free_delivery_min_price = get_setting('free_delivery_min_price', default=20)
            if total_cost <= free_delivery_min_price:
                delivery_price = get_setting('default_delivery_price', default=2)
                total_cost += delivery_price
        return total_cost

    @classmethod
    def get_status(cls, instance):
        if instance.status == 0:
            return 'In process'
        elif instance.status == 1:
            return 'Declined'
        else:
            return 'Accepted'

    def update(self, instance, validated_data):
        delivery_type = validated_data.get('deliveryType')
        validated_data['deliveryType'] = 0 if delivery_type == 'ordinary' else 1
        payment_type = validated_data.get('paymentType')
        validated_data['paymentType'] = 0 if payment_type == 'online' else 1
        status = validated_data.get('status')
        if status == 'In process':
            validated_data['status'] = 0
        elif status == 'Declined':
            validated_data['status'] = 1
        else:
            validated_data['status'] = 2
        return super().update(instance, validated_data)
