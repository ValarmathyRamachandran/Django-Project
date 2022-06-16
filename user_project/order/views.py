from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response

from .models import Order
from .serializer import OrderCheckOutSerializer, GetOrderSerializer
from cart.models import Cart
from cart.utility import token_required


class OrderCheckoutApiView(generics.GenericAPIView):
    authentication_classes = ()

    @method_decorator(token_required)
    def post(self, request, user_id, cart_id):
        try:
            data = request.data
            serializer = OrderCheckOutSerializer(data)
            user = User.objects.get(pk=user_id)
            cart = Cart.objects.get(pk=cart_id)
            book = cart.book
            print("hi", serializer, user, cart)

            address = serializer.data.get('address')
            order = Order.objects.create(user=user, book=book, address=address,
                                         quantity=cart.quantity, total_price=cart.total_price)
            order.save()
            print("order", order)
            book.quantity -= cart.quantity
            print("book", book.quantity)
            cart.delete()
            return Response({'msg': f'order placed successfully and shipping address is {order.address} ', 'Code': 200})

        except Exception as e:
            return Response({'error': str(e), 'code': 404})

    def get(self, request):
        order = Order.objects.all()
        serializer = GetOrderSerializer(instance=order, many=True)
        return Response({'Order-details': serializer.data, 'code': 200})
