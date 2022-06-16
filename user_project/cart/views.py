import logging
from book.models import Book
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response
from .custom_exceptions import BookDoesnotNotExist, UserDoesNotExist
from .models import Cart
from .serializer import AddToCartSerializer, GetCartSerializer, UpdateCartSerializer
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

    @method_decorator(token_required)
    def get(self, request, user_id):
        """
               get all items from cart.
               :param user_id:
               :param request: empty
               :return: response of cart items by user id
               """
        try:
            user = User.objects.get(pk=user_id)
            print("user", user)
            cart = Cart.objects.filter(user_id=user)

            cart_items = GetCartSerializer(instance=cart, many=True)
            print("cart_items", cart_items)
            return Response({'cart_items ': cart_items.data, 'code': 200})
        except Exception as e:
            self.logger.debug(msg=str(e))
            return Response({'msg': 'failed to fetch cart items', 'error': str(e)})

    @method_decorator(token_required)
    def patch(self, request, user_id, cart_id):
        try:
            data = request.data
            serializer = UpdateCartSerializer(data)
            quantity = serializer.data.get('quantity')
            cart = Cart.objects.get(cart_id,pk=user_id)
            cart.quantity = quantity
            cart.total_price = cart.book.price * quantity
            cart.save()
            return Response({'msg': 'cart updated successfully', 'code': 200})
        except Exception as e:
            return Response({'Error': str(e), 'Code': 404})

    @method_decorator(token_required)
    def delete(self, request, user_id, cart_id):
        try:
            cart = Cart.objects.get(pk=cart_id)
            if cart.user.id != user_id:
                raise UserDoesNotExist('This user is not authorised to update', 404)
            cart.delete()
            return Response({'msg': 'Cart items Deleted', 'code': 200})
        except UserDoesNotExist as exception:
            return Response(exception.__dict__)
        except Exception as e:
            return Response({'error': str(e), 'code': 404})
