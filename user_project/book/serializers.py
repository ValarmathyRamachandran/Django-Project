from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    # rating = serializers.IntegerField()
    # total_book_added = serializers.IntegerField()

    class Meta:
        model = Book
        fields = '__all__'


class GetBookByRatingSerializer(serializers.ModelSerializer):
    # rating = serializers.IntegerField()
    # total_book_added = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['image_field', 'name', 'author', 'price', 'rating']
