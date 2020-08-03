from .utils import PostEmail
from django.db import models
from django import forms
from django.forms import fields
from django.forms import widgets

from blog.models import Post,Category,Subscribe

class SendEmailForm(forms.Form):    
    #发送订阅邮件的表单  
    
    #选择文章
    article_id = fields.IntegerField(
        widget = widgets.Select()
    )

    #选择邮件类型，1为新发布的文章，2为更新原有文章，3为自定义内容
    email_type = fields.ChoiceField (choices=[(1,"发布"),(2,"更新"),(3,"自定义")], #单选下拉框
        initial=1)
    
    #选择3时的邮件文本
    email_context = fields.CharField (required=False)

    #得到文章的选项
    def __init__(self,*args,**kwargs):   
        super(SendEmailForm, self).__init__(*args,**kwargs)
        self.fields['article_id'].widget.choices=Post.objects.values_list('id','title')

    #获得相关数据并调用发送邮件函数PostEmail
    def save(self):
        #获得表单数据
        post_id=self.cleaned_data.get('article_id')
        email_type=self.cleaned_data.get('email_type')
        email_context=self.cleaned_data.get('email_context')
        #得到订阅相关分类的用户
        article=Post.objects.get(id=post_id)
        subs = Subscribe.objects.filter(category=article.category,clicked=True)
        for sub in subs:
            PostEmail(sub.user.username,sub.user.nickname,article,email_type,email_context)