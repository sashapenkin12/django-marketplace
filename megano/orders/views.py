import random
from string import ascii_lowercase

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from megano.settings import BASKET_SESSION_ID
from users.serializers import PaymentSerializer
from .models import Order
from .serializers import OrderSerializer, OrderProductSerializer
from users.models import Profile

class OrdersView(APIView):
    """
    API view for retrieving and creating orders.

    Attributes:
        permission_classes: Array of permissions required to access the view.

    Methods:
        get: Retrieve all user's orders.
        post: Create new order.
    """

    @classmethod
    def get(cls, request: Request):
        """
        Handles get requests.

        Args:
            request: Current HTTP request.

        Returns:
            Response: response with serialized data.
        """
        profile = Profile.objects.get(user=request.user)
        orders = Order.objects.filter(
            fullName=profile.fullName,
        ).prefetch_related('products').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request: Request):
        """
        Handles post requests.

        Args:
            request: Current HTTP request.

        Returns:
            Response: response with serialized data or 400 status code.
        """
        serializer = OrderProductSerializer(create_order=True, data=request.data, many=True)
        if serializer.is_valid():
            order_id = serializer.save()[0]
            order = Order.objects.get(pk=order_id)
            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                order.fullName = profile.fullName
                order.phone = profile.phone
                order.email = profile.email
            order.save()
            return Response({'orderId': order_id})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetConfirmOrderView(APIView):
    """
    API view for retrieving and confirming processed orders.

    Attributes:
        permission_classes: Array of permissions required to access the view.

    Methods:
        get: Retrieve order by pk.
        post: Confirm order.
    """
    @classmethod
    def get(cls, request: Request, pk: int):
        """
        Handles get requests.

        Args:
            request: Current HTTP request.
            pk: Order primary key.

        Returns:
            Response: response with serialized data or 400 status code.
        """
        order = Order.objects.prefetch_related('products').get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request: Request, pk: int):
        """
        Handles post requests.

        Args:
            request: Current HTTP request.
            pk: Order primary key.

        Returns:
            Response: response with serialized data or 400 status code.
        """
        order = Order.objects.prefetch_related('products').get(pk=pk)
        order_id = request.data.get('orderId')
        if request.data.get('orderId'):
            del request.data['orderId']
            del request.data['products']
            request.data['id'] = order_id
        serializer = OrderSerializer(order)
        serializer.update(order, request.data)
        return Response({'orderId': order.id}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    """
    API view for paying for orders.

    Attributes:
        permission_classes: Array of permissions required to access the view.

    Methods:
        post: Create new order.
    """
    @classmethod
    def post(cls, request: Request, pk: int) -> Response:
        """
        Handles post requests.

        Args:
            request: Current HTTP request.
            pk: Order primary key.

        Returns:
            Response: response with 202 status code or payment error.
        """
        serializer = PaymentSerializer(data=request.data)
        order = Order.objects.get(pk=pk)
        if serializer.is_valid():
            if str(serializer.data['number']).endswith('0'):
                order.status = 2
            else:
                order.status = 1
            serializer.save()
        else:
            order.status = 1
        order.save()
        if request.session[BASKET_SESSION_ID]:
            request.session[BASKET_SESSION_ID] = []
        if order.status == 1:
            return Response(
                {'paymentError': ''.join([random.choice(ascii_lowercase) for _ in range(10)])}
            )
        return Response(status=status.HTTP_202_ACCEPTED)
