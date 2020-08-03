from django.core.mail import send_mail
from .models import TitleRandom,AdjRandom,ContextRandom

class PostEmail():
    ''' 
    发送邮件
    1为发布新文章2为更新现有文章3为自定义内容
    '''
    def __init__(self,username,nickname,article,type,text):
        #随机内容
        context_rd=ContextRandom.objects.all().order_by('?').first()
        if type=='1':
            message = '\n'.join([
                '{1}{0}大佬您好，'.format(nickname,TitleRandom.objects.all().order_by('?').first().name),
                '{0}在‘{1}’分类发布了名为《{2}》的文章'.format(context_rd.part1,article.category,article.title),
                '{0}'.format(context_rd.part2),
                '/'.join(['http://saltfishisland.com','posts',str(article.id)]),
                '{0}'.format(context_rd.part3),
                '您{0}的，'.format(AdjRandom.objects.all().order_by('?').first().name),
                '鱼咸岛外籍大佬管理委员会'
                ])
        elif type=='2':
            message = '\n'.join([
                '{1}{0}大佬您好，'.format(nickname,TitleRandom.objects.all().order_by('?').first().name),
                '{0}更新了在‘{1}’分类下名为《{2}》的文章'.format(context_rd.part1,article.category,article.title),
                '{0}'.format(context_rd.part2),
                '/'.join(['http://saltfishisland.com','posts',str(article.id)]),
                '{0}'.format(context_rd.part3),
                '您{0}的，'.format(AdjRandom.objects.all().order_by('?').first().name),
                '鱼咸岛外籍大佬管理委员会'
                ])
        else:
            message = text       
        send_mail('鱼咸岛邮件订阅服务',message, None,[username])



        
