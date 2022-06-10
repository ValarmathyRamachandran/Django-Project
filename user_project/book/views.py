import logging
from rest_framework import generics
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


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
                return Response({'msg': 'Book name already exists', 'code': 401})

            book.save()
            return Response({'msg': 'Book Created successfully', 'data': book.data, 'code': 200})

        except Exception as e:
            self.logger.exception(msg=e)
            return Response({'msg': 'Invalid Details provided', 'code': 400})

    def get(self, request):
            """
            Get all books
            :param request:
            :return: Books
            """
            try:
                all_books = Book.objects.all()
                book_dict = BookSerializer(all_books, many=True)
                return Response({ 'msg': 'Displayed all book details', 'data': book_dict.data})

            except Exception as e:
                self.logger.exception(msg=e)
                return Response({'success': 'False', 'message': 'Error'})

    def put(self, request):
            """
            Update author_name and released date name based on book_name.
            :param request:
            :return: Json reponse of success or failure
            """

            try:

                book_object = Book.objects.get(name=request.data['name'])
                if book_object:
                    books = BookSerializer(book_object, data=request.data)
                    books.is_valid()
                    books.save()
                    return Response({'msg': 'Successfully updated book data',
                                         'data': books.data, 'code':200})
                else:
                    return Response({'msg': 'book_name does not exist', 'code': 401})

            except Exception as e:
                self.logger.exception(msg=e)
                return Response({'msg': 'error', 'code': 400})

    def delete(self, request):
            """
            Reduce the book quantity by 1  based on given book_name
            :param request:
            :return:  Response
            """

            try:
                if Book.objects.get(name=request.data['name']):
                    # book.update(quantity=quantity-1)
                    return Response({'msg': 'quantity reduced successfully', 'code': 200})
                else:
                    return Response({'msg': 'book doesnt exist', 'code': 401})
            except Exception as e:
                self.logger.exception(msg=e)
                return Response({'msg': 'book does not exists or error', 'code': 409})
