import markdown,re
from django.db import models
from users.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.conf import settings

def generate_rich_content(value):
    '''
    markdown格式
    '''
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}

class BigCategory(models.Model):
    '''
    大分类，暂未使用
    '''
    name = models.CharField(max_length=100)
    introduce = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Category(models.Model):
    '''
    分类
    '''
    name = models.CharField(max_length=100)
    #通过自定义的subscribe与user模型建立多对多关系
    subs = models.ManyToManyField(to=User, through="Subscribe", through_fields=("category", "user"))
    #简介
    introduce = models.CharField(max_length=200)
    big_cat = models.ForeignKey(BigCategory, verbose_name='大类', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    #新建分类时自动生成关系
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        users=User.objects.all()
        for user_obj in users:
            sub_obj = Subscribe(category=self, user=user_obj,clicked=False)
            sub_obj.save()

class Subscribe(models.Model):
    '''
    订阅，clicked统计是否订阅
    '''
    category = models.ForeignKey(to=Category,verbose_name='分类',on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,verbose_name='用户',on_delete=models.CASCADE)
    # 自己创建第三张表，并通过ManyToManyField指定关联
    clicked= models.BooleanField()

    class Meta:
        unique_together = ("category", "user")




class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=100)
    introduce = models.CharField(max_length=200)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    '''
    文章
    '''
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ["-created_time"]

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(
            extensions=["markdown.extensions.extra", "markdown.extensions.codehilite",]
        )
        if not self.excerpt:
            #如果未填写摘要则自动生成
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)


    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)
