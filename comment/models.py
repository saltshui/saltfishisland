from django.db import models
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from blog.models import Post
from ckeditor.fields import RichTextField


class Comment(MPTTModel):
    '''
    评论模型
    继承了mptt自带的类型
    '''
    #评论对应的文章
    article = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    #评论的用户
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    #评论内容
    body = RichTextField()
    #创建时间
    created = models.DateTimeField(auto_now_add=True)
    #评论对象（顶层评论）
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    #回复对象（回复的用户）
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
