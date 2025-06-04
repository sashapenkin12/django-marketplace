"""
A module contains serializers for users app models.
"""

from rest_framework import serializers

from .models import Profile, Image, Payment

class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for images.

    Attributes:
        src: Path to image.
        alt: Alternative content if image did not load.
    """
    src = serializers.ImageField(source='image')
    alt = serializers.CharField(source='content')

class DefaultImageSerializer(ImageSerializer):
    """
    Serializer for Image model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = Image
        fields = 'src', 'alt'

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.

    avatar: Instance of DefaultImageSerializer

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    avatar = DefaultImageSerializer()

    class Meta:
        model = Profile
        fields = 'fullName', 'email', 'phone', 'avatar'

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.

    Meta:
        model: Model of serializer.
        fields: Array of representing fields.
    """
    class Meta:
        model = Payment
        fields = '__all__'
