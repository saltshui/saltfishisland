from django.shortcuts import redirect
from .forms import RegisterForm,ReactiveEmailForm,AuthLoginForm,ResetEmailForm,ResetConfirmForm,PasswordChangeForm
from .models import User
from .utils import Token,anonymous_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,FormView,TemplateView
from django.conf import settings
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.http import Http404
from django.contrib import messages

token_confirm = Token(settings.SECRET_KEY)

@method_decorator(anonymous_required, name='dispatch')
class LoginView(LoginView):
    '''
    修改登陆界面，加入验证码
    '''
    template_name = 'users/login.html'
    form_class = AuthLoginForm


class BasicLoginView(LoginView):
    '''
    定制特殊情况(modal内)的登陆界面，删除了前往其他界面的链接
    '''
    template_name = 'users/basiclogin.html'
    form_class = AuthLoginForm


class TokenFormView(FormView):
    '''
    生成动态口令的视图函数
    会多次使用所以单独提取出来。继承自Django自带的FormView，修改了form_valid()
    '''
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        #生成动态口令
        token = token_confirm.generate_validate_token(username)
        #将口令传输到form并由form.save()调用邮件函数发送邮件
        self.object = form.save(token)
        return super().form_valid(form)
    
@method_decorator(anonymous_required, name='dispatch')
class RegisterView(TokenFormView):
    '''
    注册界面
    注册成功后发送验证邮件并跳转到邮件发送成功界面
    '''
    template_name = 'users/register.html'
    form_class = RegisterForm
    def get_success_url(self):        
        return 'emailsent/done'
        

def active_user(request,token):
    '''
    用户激活函数
    '''
    try:
        #如果可以从口令得到用户名则获取用户名否则跳转到404
        username = token_confirm.confirm_validate_token(token)
    except:
        raise Http404
    try:
        #如果该用户名存在则获取调用用户模型否则跳转到404
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    #将用户状态改为激活并保存
    user.is_active = True
    user.save()
    #返回激活成功界面您已经成功激活
    messages.add_message(request, messages.SUCCESS, '您已经成功激活！欢迎来到鱼咸岛！', extra_tags='success')

    return redirect('/')

@method_decorator(anonymous_required, name='dispatch')
class ReactiveView(TokenFormView):
    '''
    重新发送激活邮件的界面
    发送邮件并跳转到邮件发送成功界面
    '''
    template_name = 'users/reactive.html'
    form_class = ReactiveEmailForm
    def get_success_url(self):        
        return 'emailsent/done'        

@method_decorator(anonymous_required, name='dispatch')
class EmailConfirmDoneView(TemplateView):
    '''
    激活邮件发送成功的界面
    '''
    template_name = 'users/email_confirm_done.html'


@method_decorator(anonymous_required, name='dispatch')
class ResetEmailDoneView(TemplateView):
    '''
    重置密码邮件发送成功的界面
    '''
    template_name = 'users/password_reset_done.html'
    
@method_decorator(anonymous_required, name='dispatch')
class PasswordResetView(TokenFormView):      
    '''
    发送重置密码邮件的界面
    发送邮件并跳转到邮件发送成功界面
    '''
    template_name = 'users/password_reset_form.html'
    form_class = ResetEmailForm
    def get_success_url(self):        
        return 'emailsent/done'
        
@method_decorator(anonymous_required, name='dispatch')    
class PasswordResetConfirmView(FormView):
    '''
    重置密码的界面
    '''
    template_name = 'users/password_reset_confirm.html'
    form_class = ResetConfirmForm
               
    def get_form_kwargs(self):
        #得到从url传入的口令
        token=self.kwargs.get('token')
        try:
            username = token_confirm.confirm_validate_token(token)
        except:
            raise Http404
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        #将对应的用户传到form便于验证密码有效性

        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': user,
        })
        return kwargs

    #验证表单有效后调用save储存密码,跳转到主页,提示密码设置成功
    def form_valid(self, form):
        form.save()
        """If the form is valid, redirect to the supplied URL."""
        messages.add_message(self.request, messages.SUCCESS, '修改密码成功！', extra_tags='success')    
        return redirect('/')  
    

class PasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    '''
    修改密码
    '''
    form_class = PasswordChangeForm
    template_name = 'users/password_change_form.html'
    login_url = '/users/login/'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, '修改密码成功！', extra_tags='success')    
        return redirect('/')  


