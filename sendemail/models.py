from django.db import models

# Create your models here.

'''
让订阅邮件更多样性一点，大概
每次发送邮件随机从数据库中取出数据进行组合
'''
class TitleRandom(models.Model):
    '''
    邮件开头称呼
    '''
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '称呼'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AdjRandom(models.Model):
    '''
    邮件落款称呼
    '''
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '落款修饰'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ContextRandom(models.Model):
    '''
    邮件正文，分为3部分
    '''
    part1 = models.CharField(max_length=500)
    part2 = models.CharField(max_length=500)
    part3 = models.CharField(max_length=500)
    
    class Meta:
        verbose_name = '内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.part1