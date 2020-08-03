from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,SetPasswordForm
from .models import User
from blog.models import Category,Subscribe
from django import forms
from .utils import Confirm_Email
from captcha.fields import CaptchaField
from django.contrib.auth import password_validation

class EmailUsernameForm(forms.Form):
    '''
    发送邮件的表单
    '''
    username = forms.EmailField(
        label="电子邮箱",
        help_text="<ul><li>请输入您注册时使用的电子邮箱</li></ul>",
        max_length=150,
        widget=forms.EmailInput(attrs={'autofocus':'True','autocomplete': 'email','class': 'form-control','placeholder':'电子邮箱'})
    )

    captcha = CaptchaField(label='验证码')
    

class RegisterForm(UserCreationForm):
    '''
    注册界面的表单
    '''
    #翻译错误信息及帮助信息
    error_messages = {
        'password_mismatch': '密码不匹配，请输入相同的密码',
    }
    password1 = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control','placeholder':'密码'}),
        help_text='<ul><li>您的密码不能与用户名或昵称过于相似</li>'
        '<li>您的密码必须包含至少 8 个字符</li>'
        '<li>您的密码不能过于常见</li>'
        '<li>您的密码不能仅包含数字</li></ul>',
        )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control','placeholder':'确认密码'}),
        strip=False,
        help_text="<ul><li>请输入相同的密码</li></ul>",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        #增加自定义的昵称字段
        fields = ("username","nickname")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['class'] = 'form-control'
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['placeholder'] = '电子邮箱'
        self.fields["nickname"].widget.attrs['class'] = 'form-control'
        self.fields["nickname"].widget.attrs['placeholder'] = '昵称'
        self.fields["nickname"].help_text = "<ul><li>昵称设定后暂时无法更改</li></ul>" 

    def save(self,token, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #默认为未激活
        user.is_active=False
        #发送验证邮件
        Confirm_Email(user.username,user.nickname,token,1)
        if commit:
            user.save()
            #生成订阅信息，默认不订阅
            cat=Category.objects.all()
            for cat_obj in cat:
                sub_obj = Subscribe(category=cat_obj, user=user,clicked=False)
                sub_obj.save()
        return user

class AuthLoginForm(AuthenticationForm):
    '''
    为登陆界面增加验证码验证
    '''
    error_messages = {
        'inactive':'该用户尚未激活，请先激活',
        'invalid_login': "请输入正确的电子邮箱和密码",      
    }
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control','placeholder':'用户名'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class': 'form-control','placeholder':'密码'}),
    )
    captcha = CaptchaField(label='验证码',
        help_text='<ul><li>输入表达式的结果（数字）</li><li>点击图片刷新验证码</li></ul>',
        )
    
    def clean(self):
        '''
        重写验证函数，在未激活且正确输入密码时提示需要激活
        '''
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')        
        if username is not None and password:
            try:
                user = User._default_manager.get_by_natural_key(username)
            except User.DoesNotExist:
                raise self.get_invalid_login_error()
            if user.check_password(password):
               self.user_cache=user
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data



class ReactiveEmailForm(EmailUsernameForm):
    '''
    重新发送激活邮件的表单
    '''
    def save(self,token):
        username = self.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                nickname=user.nickname
            except User.DoesNotExist:
                nickname=0
            if nickname and user.is_active==False:
                Confirm_Email(username,nickname,token,1)


class ResetEmailForm(EmailUsernameForm):
    '''
    发送重置密码邮件的表单
    '''
    def save(self,token):
        username = self.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                nickname=user.nickname
            except User.DoesNotExist:
                nickname=0
            if nickname and user.is_active:
                Confirm_Email(username,nickname,token,2)


class SetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': '密码不匹配，请输入相同的密码',
    }    
    new_password1 = forms.CharField(
        label="新密码",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete': 'new-password','class': 'form-control','placeholder':'密码'}),
        help_text='<ul><li>您的密码不能与用户名或昵称过于相似</li>'
        '<li>您的密码必须包含至少 8 个字符</li>'
        '<li>您的密码不能过于常见</li>'
        '<li>您的密码不能仅包含数字</li></ul>',
        )
    new_password2 = forms.CharField(
        label="确认密码",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control','placeholder':'确认密码'}),
    )

class ResetConfirmForm(SetPasswordForm):
    '''
    重置密码的表单
    '''

    #获取从view中传入的user信息
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(self.user, *args, **kwargs)

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "旧密码有误，请重新输入",
    }
    old_password = forms.CharField(
        label="旧密码",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'class': 'form-control','placeholder':'旧密码'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
