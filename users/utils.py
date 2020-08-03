from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def anonymous_required(function=None, redirect_url=None):
    '''
    修饰器，仅允许未登录用户
    '''
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


class Token():
    '''
    口令相关函数
    '''
    def __init__(self,security_key):
        #初始化，根据自身security_key生成salt
        self.security_key = security_key
        self.salt = base64.encodestring(security_key.encode())

    def generate_validate_token(self,username):
        #生成口令的函数
        serializer = utsr(self.security_key)
        return serializer.dumps(username,self.salt)
  
    def confirm_validate_token(self,token,expiration=settings.TOKEN_EXPIRATION):
        #验证口令的函数
        serializer = utsr(self.security_key)
        return serializer.loads(token,salt=self.salt,max_age=expiration)

class Confirm_Email():
    '''
    发送验证邮件的函数
    分为1激活账号2重置密码
    '''
    def __init__(self,username,nickname,token,type):

        if type==1:
            message = "\n".join([
            '尊贵的{0}大佬:'.format(nickname),
            '您好,欢迎办理鱼咸岛登岛手续',
            '请访问该链接，验证您的身份:',
            '/'.join(['http://saltfishisland.com','users/activate',token]),
            '如非您本人操作，请忽略该邮件',
            '感谢您对鱼咸岛外籍大佬管理委员会工作的支持',
            '',
            '正在摸鱼的',
            '鱼咸岛外籍大佬管理委员会',      
            ])
        if type==2:
            message = "\n".join([
            '尊敬的{0}大佬:'.format(nickname),
            '您好,您正在办理鱼咸岛密码修改业务',
            '请访问该链接，修改您的密码:',
            '/'.join(['http://saltfishisland.com','users/password_reset',token]),
            '如非您本人操作，请忽略该邮件',
            '感谢您对鱼咸岛外籍大佬管理委员会工作的支持',
            '',
            '您忠诚的',
            '鱼咸岛外籍大佬管理委员会',  
            ])
        send_mail('鱼咸岛登岛手续',message, None,[username])


        
