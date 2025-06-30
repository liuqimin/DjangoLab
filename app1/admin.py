from django.contrib import admin

# Register your models here.
from import_export.admin import ExportMixin
from import_export import resources
from .models import Books

class BooksResource(resources.ModelResource):
    class Meta:
        model = Books
        fields = ("id","title","content")


class BooksAdmin(ExportMixin,admin.ModelAdmin):
    resource_classes = BooksResource
    list_display = ("id","title")
    search_fields = ("title",)
    list_filter = ("title",)

    def get_export_resource_classes(self, request):
        return [BooksResource]  # ✅ 必须是可迭代对象

admin.site.register(Books, BooksAdmin)