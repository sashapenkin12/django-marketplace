"""
Products app serializer
"""
from .models import Product, ProductImage, Subcategory, Category, Specification, Tag, Sale, Review
from rest_framework import serializers
from users.serializers import ImageSerializer, DefaultImageSerializer


class ProductImageSerializer(ImageSerializer):
    """
    Serializer for ProductImage model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = ProductImage
        fields = 'src', 'alt'


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = Tag
        fields = 'id', 'name',


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Subcategory model.

    Attributes:
        image: Image serializer.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """

    image = DefaultImageSerializer()
    class Meta:
        model = Subcategory
        fields = 'id', 'title', 'image'


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.

    Attributes:
        subcategories: Subcategories serializer.
        image: Image serializer.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    subcategories = SubCategorySerializer(many=True)
    image = DefaultImageSerializer()

    class Meta:
        model = Category
        fields = 'id', 'title', 'image', 'subcategories'


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Specification model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = Specification
        fields = 'name', 'value'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'rate', 'date')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.

    Attributes:
        images: Images serializer.
        tags: Tags serializer.
        specifications: Specification serializer.
        reviews: Number of product reviews that defined by method.

    Methods:
        get_reviews: Get number of reviews on product instance.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.

    """
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    @classmethod
    def get_reviews(cls, instance):
        """
        Method that returns Product instance reviews count.

        Returns:
            int: Number of reviews.
        """
        return instance.reviews.count()


    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date',
                  'title', 'description', 'fullDescription', 'freeDelivery', 'images', 'tags',
                  'reviews', 'rating', 'specifications')


class ProductWithReviewsSerializer(ProductSerializer):
    """
    Serializer for Product model that represents reviews of instance.

    Attributes:
        reviews: Reviews serializer.
    """
    reviews = ReviewSerializer(many=True)


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for Sale model.

    Attributes:
        price: Sale product price.
        title: Sale product title.
        images: Sale product images.
        id: Sale product id.

    Methods:
        get_price: Get product price.
        get_title: Get product title.
        get_images: Get product images.
        get_id: Get product id.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.

    """
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    @classmethod
    def get_price(cls, instance):
        return instance.product.price

    @classmethod
    def get_title(cls, instance):
        return instance.product.title

    @classmethod
    def get_images(cls, instance):
        serializer = ProductImageSerializer(instance.product.images, many=True)
        return serializer.data

    @classmethod
    def get_id(cls, instance):
        return instance.product.pk


    class Meta:
        model = Sale
        fields = 'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
