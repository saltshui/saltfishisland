from django.contrib import admin
from .models import Post, Category, Tag, Subscribe,BigCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category','views']
    fields = ['title', 'body', 'excerpt', 'category', 'tags', 'created_time','views']
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class CatAdmin(admin.ModelAdmin):
    def subs_cnt(self,obj):
        return [Subscribe.objects.filter(category=obj,clicked=True).count()]
    list_display = ['name','subs_cnt']

class SubsAdmin(admin.ModelAdmin):
    list_display = ['category','user','clicked']
    list_filter = ('clicked',)

admin.site.register(Post, PostAdmin)
admin.site.register(BigCategory)
admin.site.register(Category,CatAdmin)
admin.site.register(Tag)
admin.site.register(Subscribe,SubsAdmin)
