from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Book,Author,Category
from .serializers import BookSerializers,AuthorSerializers,CategorySerializers

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