from django.db import models
from django.conf import settings
'''
class meta所有属性
abstract	bool	声明是否为抽象模型类
db_table	str	指定数据库表名
ordering	list	设置默认排序方式
verbose_name	str	单数显示名称（如后台管理界面）
verbose_name_plural	str	复数显示名称
permissions	list	添加自定义权限
unique_together	tuple/list	联合唯一约束
index_together	tuple/list	联合索引（已废弃，推荐用 indexes）
default_related_name	str	设置反向关联默认名称
get_latest_by	str	设置 latest() 默认排序字段
constraints	list	新版约束（如唯一、条件等）
indexes	list	自定义数据库索引
managed	bool	是否由 Django 管理数据库表
app_label	str	指定模型归属的 app（跨 app 建模时用）
'''
# Create your models here.
class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        on_delete = models.SET_NULL,
        null=True, blank = True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        abstract = True # 抽象类,不生成表

class Author(AuditModel):
    name = models.CharField(max_length= 100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 分类表
class Category(AuditModel):
    name = models.CharField(max_length=100,
                            unique=True)
    def __str__(self):
        return self.name
    
# 图书表
class Book(AuditModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, 
                               on_delete=models.CASCADE,
                               related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")
    published_at = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.title

































































































































