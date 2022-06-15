import logging
from book.models import Book
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response
from .custom_exceptions import BookDoesnotNotExist, UserDoesNotExist
from .models import Cart
from .serializer import AddToCartSerializer
from .utility import token_required


class AddToCart(generics.GenericAPIView):
    authentication_classes = ()
    logger = logging.getLogger(__name__)
    serializer_class = AddToCartSerializer

    @method_decorator(token_required)
    def post(self, request, user_id):
        """
        Add items to cart.
        :param user_id:
        :param request: cart item data
        :return: response of cart added
        """
        try:
            data = request.data
            serializer = AddToCartSerializer(data)

            user_data = dict(serializer.data)
            book_id = user_data.get('book_id')
            quantity = user_data.get('quantity')
            books = Book.objects.get(pk=book_id)
            print('book', books)
            if not books:
                raise BookDoesnotNotExist('Book does not Exist', 404)
            total_price = books.price * quantity
            user = User.objects.get(pk=user_id)
            print("hello", user)
            if not user:
                raise UserDoesNotExist('User does not Exist', 404)
            cart = Cart.objects.create(user_id=user, book_id=books, quantity=quantity, total_price=total_price)
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
