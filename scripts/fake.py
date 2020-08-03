import os
import pathlib
import random
import sys
from datetime import timedelta
 
import django
import faker
from django.utils import timezone

#用法:python -m scripts.fake

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
 
    from blog.models import BigCategory,Category, Post, Tag
    from comment.models import Comment
    from users.models import User

    big_category_list = ['学习笔记', '开源项目', 'story','test category']
    category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    tag_list = ['django', 'Python', '动物森友会', 'Docker', 'Nginx', 'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
    a_year_ago = timezone.now() - timedelta(days=365)
 
    user=User.objects.get(username='a@b.cc')
 
    print('create categories and tags')
    fake = faker.Faker()  # English
    
    for bcate in big_category_list:
        BigCategory.objects.create(name=bcate,introduce=fake.paragraph())
 
 
    for cate in category_list:
        bcate = BigCategory.objects.order_by('?').first()        
        Category.objects.create(name=cate,big_cat=bcate,introduce=fake.paragraph())
 
    for tag in tag_list:
        Tag.objects.create(name=tag,introduce=fake.paragraph())
 
    print('create a markdown sample post')
    Post.objects.create(
        title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试',
                                         big_cat=BigCategory.objects.create(name='Markdown测试',introduce=fake.paragraph()),
                                         introduce=fake.paragraph()),
        author=user,
    )

    print('create some faked posts published within the past year')
    for _ in range(100):
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    fake = faker.Faker('zh_CN')
    for _ in range(100):  # Chinese
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            user = User.objects.order_by('?').first()
            Comment.objects.create(
                user=user,               
                body=fake.paragraph(),
                created=fake.date_time_between(
                     start_date=delta_in_days, 
                     end_date="now", 
                     tzinfo=timezone.get_current_timezone()),
                article=post,
            )
    print('create some reply')
    for comment in Comment.objects.all()[:20]:
        created_time = comment.created
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            user = User.objects.order_by('?').first()
            Comment.objects.create(
                user=user,
                parent_id = comment.get_root().id,
                reply_to = User.objects.order_by('?').first(),              
                body=fake.paragraph(),
                created=fake.date_time_between(
                     start_date=delta_in_days, 
                     end_date="now", 
                     tzinfo=timezone.get_current_timezone()),
                article=post,
            )
 
    print('done!')