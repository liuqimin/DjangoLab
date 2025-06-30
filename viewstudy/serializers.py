from rest_framework import serializers

from .models import Book,Author,Category


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"



class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"