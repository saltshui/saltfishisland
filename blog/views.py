from django.contrib import messages
from django.db.models import Q 
from comment.models import Comment
from comment.forms import CommentForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Tag 

from django.views.generic import ListView, DetailView,TemplateView
from pure_pagination.mixins import PaginationMixin

class FrontView(TemplateView):
    '''
    首页
    '''
    template_name = 'blog/front.html'


class ContactView(TemplateView):
    '''
    联系方式
    '''
    template_name = 'blog/contact.html'


class IndexView(PaginationMixin,ListView):
    '''
    目录
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class ArchiveView(IndexView):
    '''
    归档
    '''
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                    created_time__month=month)

class CategoryView(IndexView):
    '''
    分类
    '''
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    '''
    标签
    '''    
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)

class PostDetailView(DetailView):
    '''
    详情
    '''
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        comment_form = CommentForm()
        context['comments']=Comment.objects.filter(article=pk)
        context['comment_form']=comment_form

        return context

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
