from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from blog.models import Subscribe

class UserAdmin(UserAdmin):
    '''
    定制用户管理界面
    '''
    #获取用户订阅信息
    def subs_show(self,obj):
        return [sub.category.name for sub in Subscribe.objects.filter(user=obj,clicked=True)]
 
    #自定义用户详情界面的信息
    fieldsets = (
        (None, {'fields': ('username', 'password','nickname')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_superuser'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    #在用户列表界面显示用户名昵称激活状态及订阅信息
    list_display = ('username', 'nickname', 'is_active','subs_show')
    #允许使用是否激活来筛选用户
    list_filter = ('is_active',)
    #搜索栏可根据用户名和昵称进行搜索
    search_fields = ('username', 'nickname')
    
    filter_horizontal = ('user_permissions',)

#在管理界面注册相关模型
admin.site.register(User,UserAdmin)
