import io
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Book,Author,Category,Sales
from .serializers import BookSerializers,AuthorSerializers,CategorySerializers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.http import HttpResponse
# Create your views here.


class BookListCreateView(mixins.ListModelMixin, 
                         mixins.CreateModelMixin,
                         GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request)
    
    # perform_create() 是什么？
    """
        perform_create() 是 Django REST Framework（DRF） 在类视图中用于拦截并自定义保存逻辑的钩子方法，通常用于：

        设置非前端传入的字段（如 created_by, created_at）

        添加日志、触发通知

        更复杂的保存逻辑（如连带保存子表）

        ✅ 一、它在哪些类中使用？
        你可以在以下视图类中定义 perform_create()

        视图类	用途
        CreateAPIView	创建单个对象
        GenericAPIView + mixins.CreateModelMixin	也是用这个钩子
        ModelViewSet（POST）	内部也是用它

    """
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by = user)



class BookRetrieveUpdateDestoryView(mixins.RetrieveModelMixin,

                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
    
    def put(self, request, *args, **kwargs):
        return self.update(request)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request)

    def perform_update(self,serializer):
        serializer.save(updated_by=self.request.user)



class AuthorRetrieveCreateView(mixins.RetrieveModelMixin,
                                    #mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
    
    def put(self, request, *args, **kwargs):
        return self.update(request)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request)
    

class CategoryRetrieveCreateView(mixins.RetrieveModelMixin,
                                   #mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)
    
    def put(self, request, *args, **kwargs):
        return self.update(request)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request)
    



# 上传csv文件并用pandas分析

class CSVUploadAPIView(APIView):
    parser_classes = [MultiPartParser]
    '''
    parser_classes 是 用来指定请求的数据格式解析器parser的。

    MultiPartParser 是一种 专门用于解析表单上传文件如 CSV、图片、Excel 的解析器。
    POST /api/upload-csv/
    Content-Type: multipart/form-data
    Body:
    file: my_data.csv
    DRF 默认使用的是 JSONParser（只解析 application/json），那就没办法处理上传的文件了
    '''
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return Response({'error':'please upload a valid csv file'}, 
                    status=status.HTTP_400_BAD_REQUEST)
        try:
            df = pd.read_csv(file)
            summary = df.describe.to_dict()
            return Response({'summary':summary})
        except Exception as e:
            return Response({'error': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                            

#带下载
class ExportExcelAPIView(APIView):
    def get(sefl, request, *args, **kwargs):
        # 模拟data
        data = [{'name':'alice','score':90}, {'name':'Bob','score':75}]
        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')

        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type = 'applicaton/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        )
        response['Content-Disposition'] = 'attachment: filename="report.xlsx"'
        return response
    


class SalesSummaryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sales_data = Sales.objects.values('product','quantity','date')
        df = pd.DataFrame(sales_data)
        if df.empty:
            return Response({'summary':{}})
        result = df.groupby('product')['quantity'].sum().to_dict()

        return Response({'sales_summary': result})
