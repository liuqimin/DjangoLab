from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Books
from .serializers import BooksSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class BookCursporPagination(CursorPagination):
    """
    为什么用 CursorPagination？
    优点	说明
    更稳定	不受数据插入、删除影响，避免“跳页错乱”问题
    更适合实时列表	比如“下一页评论”流式加载
    安全性好	页码加密，不暴露数据库主键或偏移量
    """
    page_size = 1 
    ordering = '-id' #默认按id倒序分页
    page_size_query_param = 'size'  # 支持用户自定义分页大小 ?size=20

#page=1
class BookListCreateView(APIView):
    @swagger_auto_schema(
            query_serializer=BooksSerializer,
            response={200,'ok'}
    )
    def get(self, request):
        books = Books.objects.all()

        # 分页器
        paginator = PageNumberPagination()
        paginator.page_size = 1
        result_page = paginator.paginate_queryset(books, request)
        # 分页器 over
        # result_page为查询结果,但是不用分页的话,使用object.all
        serializer = BooksSerializer(result_page,
                                     many=True
                                     )
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
#  limit/offset的偏离值
#  ?limit=5&offset=10
class BookListTwoCreateView(APIView):
    def get(self, request):
        books = Books.objects.all()

        # 分页器
        paginator = LimitOffsetPagination()
        # paginator.page_size = 1
        result_page = paginator.paginate_queryset(books, request)
        # 分页器 over
        # result_page为查询结果,但是不用分页的话,使用object.all
        serializer = BooksSerializer(result_page,
                                     many=True
                                     )
        
        return Response(serializer.data)

# 自定义分页器
# 下一页的
class BookListCursorCreateView(APIView):
    def get(self, request):
        books = Books.objects.all()

        # 分页器
        paginator = BookCursporPagination()
        # paginator.page_size = 1
        result_page = paginator.paginate_queryset(books, request)
        # 分页器 over
        # result_page为查询结果,但是不用分页的话,使用object.all
        serializer = BooksSerializer(result_page,
                                     many=True
                                     )
        
        return Response(serializer.data)
    
class BookDetailView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book)
        return Response(serializer.data)
    
    def put(self,request, pk):
        book = get_object_or_404(Books,pk =pk)
        serializer = BooksSerializer(book, datra=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        
        book = get_object_or_404(Books,pk = pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)