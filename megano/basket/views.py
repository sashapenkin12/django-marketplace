"""
Views for the basket app.
"""

from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from .misc import get_and_serialize_product

class BasketView(APIView):
    """
    API view for getting basket and adding products to it.

    Methods:
        get: Get current basket.
        post: Add product to the basket.
        delete: Remove item from the basket.
    """
    def get(self, request: Request):

        """
        Handles get requests.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with current basket data.
        """
        basket = request.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = []
            request.session[settings.BASKET_SESSION_ID] = basket
        return Response(basket)


    def post(self, request: Request):
        """
        Handles post requests.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with updated basket data.
        """
        product_id, count = request.data['id'], int(request.data['count'])
        basket = request.session.get(settings.BASKET_SESSION_ID)

        if basket:
            for index, product in enumerate(basket):
                if product.get('id') == product_id:
                    basket[index]['count'] += count
                    break
            else:
                product = get_and_serialize_product(product_id)
                product['count'] = count
                basket.append(product)
        else:
            product = get_and_serialize_product(product_id)
            product['count'] = count
            basket = [product]
        request.session[settings.BASKET_SESSION_ID] = basket
        return Response(basket, status=201)

    def delete(self, request: Request):
        """
        Handles delete requests.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with updated basket data.
        """
        product_id, count = int(request.data['id']), int(request.data['count'])
        basket = request.session.get(settings.BASKET_SESSION_ID)
        if basket:
            for index in range(len(basket)):
                if basket[index]['id'] == product_id:
                    basket[index]['count'] -= count
                    if basket[index]['count'] == 0:
                        basket.pop(index)
        else:
            basket = []
        request.session[settings.BASKET_SESSION_ID] = basket
        return Response(basket, status=200)
