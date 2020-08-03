from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from blog.models import Subscribe


class SubscribeListView(LoginRequiredMixin,ListView):
    '''
    显示订阅列表的视图
    '''
    #在template中调用的名称
    context_object_name = 'subscribe'
    #template位置
    template_name = 'subscribe/list.html'
    #登录重定向
    login_url = '/users/login/'

    #已订阅列表
    def get_queryset(self):
        return Subscribe.objects.filter(user=self.request.user,clicked=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #未订阅列表
        context['All']=Subscribe.objects.filter(user=self.request.user,clicked=False)
        return context
    

    
class SubscribeUpdateView(LoginRequiredMixin,View):
    '''
    更新订阅信息
    '''
    login_url = '/users/login/'
  
    def get(self, request):
        #获取操作类型
        update_type=request.GET.get('update_type')
        #如果为单独操作，获取相关id
        subs_id = request.GET.get('subs_id')
        #全部订阅
        if update_type=='1':
            subs = Subscribe.objects.filter(user=self.request.user,clicked=False)
            for sub_obj in subs:
                sub_obj.clicked = True
                sub_obj.save()
        #全部取关
        elif update_type=='2':
            subs = Subscribe.objects.filter(user=self.request.user,clicked=True)
            for sub_obj in subs:
                sub_obj.clicked = False
                sub_obj.save()
        #单独订阅或取关
        else:
            Sub=Subscribe.objects.get(id=subs_id)
            if Sub.clicked == False:
                Sub.clicked=True
            else:
                Sub.clicked=False
            Sub.save()
        #操作完成后刷新页面
        return redirect('subscribe:list')