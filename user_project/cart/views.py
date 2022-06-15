import logging

import book
import jwt
import kwargs as kwargs
from book.models import Book
from django.contrib import messages
from django.contrib.auth.models import User
from prompt_toolkit.filters import app
from rest_framework import generics, request
from rest_framework.response import Response

from .models import Cart

from .serializer import AddToCartSerializer, GetCartSerializer
from .utility import  token_required


class AddToCart(generics.GenericAPIView):
    authentication_classes = ()
    logger = logging.getLogger(__name__)
    serializer_class = AddToCartSerializer

    def post(self, request):
        """
        Add items to cart.
        :param request: cart item data
        :return: response of cart added
        """
        try:
            user = token_required(request)
            data = request.data
            cart = AddToCartSerializer(data)

            cart_data = dict(cart.data)
            # print("cart", cart_data)
            book_id = cart_data.get('book_id')
            quantity = cart_data.get('quantity')
            books = Book.objects.get(id=book_id)
            total_price = books.price * quantity
            user_id = User.objects.get(id=user)
            cart = Cart.objects.create(user_id=user_id, book_id=books, quantity=quantity, total_price=total_price)
            cart.save()
            return Response({'msg': f'{books.name} added to cart successfully', 'code': 200})

        except Exception as e:
            return Response({'error': str(e), 'code': 404})

    # def get(self, request):
    #     """
    #            get all items from cart.
    #            :param request: empty
    #            :return: response of cart items
    #            """
    #     try:
    #         user_id = token_required(request)
    #         user = User.objects.get(user_id)
    #         cart = Cart.objects.filter(user=user)
    #         cart_objects = GetCartSerializer(cart, many=True)
    #         return Response({'msg': 'added to cart', 'data': cart_objects.data})
    #     except Exception as e:
    #         self.logger.debug(msg=str(e))
    #         print(str(e))
    #         return Response({'msg': 'failed to fetch data', 'error': str(e)})
