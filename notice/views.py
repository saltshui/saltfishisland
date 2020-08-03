from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post
from django.http import Http404

class CommentNoticeListView(LoginRequiredMixin,ListView):
    '''
    通知列表
    '''
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = '/users/login/'

    #未读通知
    def get_queryset(self):
        return self.request.user.notifications.unread()

    #已读通知
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readed']=self.request.user.notifications.read()

        return context

class CommentNoticeUpdateView(LoginRequiredMixin,View):
    '''
    更新通知
    '''
    login_url = '/users/login/'

    def get(self, request):
        #获取相关id
        notice_id = request.GET.get('notice_id')
        article_id = request.GET.get('article_id')

        #更新单条通知
        if notice_id:
            if not article_id:
                raise Http404
            try:
                #如果该文章存在则获取否则跳转到404
                article = Post.objects.get(id=article_id)           
            except Post.DoesNotExist:
                raise Http404
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        #更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')