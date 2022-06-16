import logging

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, GetBookByRatingSerializer
from django.core.paginator import Paginator

from user_project.settings import CACHE_TTL


class AddBookAPI(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = BookSerializer
    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        Get book details from user and create book
        :param request:
        :return:  response of book added or not
        """

        try:
            book = BookSerializer(data=request.data)
            book.is_valid()

            if Book.objects.filter(name=request.data['name']).exists():
                book = Book.objects.get(quantity=request.data['quantity'],
                                        total_book_added=request.data['total_book_added'])
                book.quantity = book.total_book_added + book.quantity
                return Response(
                    {'msg': 'Book name already exists ,so added the given quantity', 'code': 401,
                     'quantity': book.quantity})

            book.save()
            return Response({'msg': 'Book Created successfully', 'data': book.data, 'code': 200})

        except Exception as e:
            self.logger.exception(msg=e)
            return Response({'msg': 'Invalid Details provided', 'code': 400})

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, id=None):
        """
            Get all books
            :param id:
            :param request:
            :return: Books
            """

        try:
            if id:
                book = Book.objects.get(pk=id)
                serializer = GetBookByRatingSerializer(book)
                return Response({'Data': serializer.data, 'Code': 200})
            all_books = Book.objects.order_by('-rating')
            # all_books = Book.objects.all()
            book_dict = GetBookByRatingSerializer(all_books, many=True)
            paginator = Paginator(all_books, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return Response(
                {'msg': 'Displayed all book details by rating order', 'data': book_dict.data, 'page': str(page_obj)})

        except Exception as e:
            self.logger.exception(msg=e)
            return Response({'msg': 'Error', 'code': 401})

    def put(self, request):
        """
            Update author name and released date name based on book name.
            :param request:
            :return: reponse of success or failure
            """

        try:

            book_object = Book.objects.get(name=request.data['name'])
            if book_object:
                books = BookSerializer(book_object, data=request.data)
                books.is_valid()
                books.save()
                return Response({'msg': 'Successfully updated book data',
                                 'data': books.data, 'code': 200})
            else:
                return Response({'msg': 'book_name does not exist', 'code': 401})

        except Exception as e:
            self.logger.exception(msg=e)
            return Response({'msg': 'error', 'code': 400})

    def delete(self, request):
        """
            Reduce the book quantity based on given book_name
            :param request:
            :return:  Response
            """

        try:
            if Book.objects.get(name=request.data['name']):
                book = Book.objects.get(quantity=request.data['quantity'],
                                        total_book_added=request.data['total_book_added'])
                book.quantity = book.total_book_added - book.quantity
                return Response(
                    {'msg': 'Given quantity of book was reduced successfully', 'code': 200, 'quantity': book.quantity})
            else:
                return Response({'msg': 'book doesnt exist', 'code': 401})
        except Exception as e:
            self.logger.exception(msg=e)
            return Response({'msg': 'book does not exists or error', 'code': 409})
