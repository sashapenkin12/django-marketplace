"""
Misc functions for basket app.
"""
from products.models import Product
from products.serializers import ProductSerializer

def get_and_serialize_product(product_id: int) -> dict:
    """
    Get and serialize product

    Args:
        product_id: Product primary key.

    Returns:
        dict: Serialized product data.
    """
    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product)
    return serializer.data
