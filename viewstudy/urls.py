from django.urls import path

from .views import (
    BookListCreateView,
    BookRetrieveUpdateDestoryView,
    CategoryRetrieveCreateView,
    AuthorRetrieveCreateView,
    CSVUploadAPIView,
    ExportExcelAPIView
)

urlpatterns = [
    path('books/',BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>', BookRetrieveUpdateDestoryView.as_view(), name='book-detail'),
    path('category/<int:pk>', CategoryRetrieveCreateView.as_view(), name='Categorydetail'),
    path('author/<int:pk>', AuthorRetrieveCreateView.as_view(), name='Author-detail'),
    path('api/upload-csv',CSVUploadAPIView.as_view(), name = 'uplopad_csv_api'),
    path('api/export-excel/', ExportExcelAPIView.as_view(), name='export_excel_api'),
    ]