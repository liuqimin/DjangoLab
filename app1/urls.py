from django.urls import path
from .views import BookListCreateView,BookDetailView, BookListTwoCreateView

urlpatterns = [
    path('books/',BookListCreateView.as_view(), name='BookContent'),
    path('booksTwo/',BookListTwoCreateView.as_view(), name='BookContent'),
    path('books/<int:pk>',BookDetailView.as_view(), name='book-detail'),
]