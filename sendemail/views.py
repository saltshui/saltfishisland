from django.shortcuts import render,redirect
from django.views import View
from django.http import Http404
from .forms import SendEmailForm
from django.contrib import messages

def superuser_only(function):
    #超级用户修饰器
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
            #如果不是管理员则返回404假装这一页没有东西
        return function(request, *args, **kwargs)
    return _inner

@superuser_only
def SendSubEmail(request):
        
    if request.method == 'POST':      
        form = SendEmailForm(request.POST)
        if form.is_valid():
            form.save()    
            messages.add_message(request, messages.SUCCESS, '发送成功！', extra_tags='success')
            return redirect('/')
    else:
        form = SendEmailForm()
 
    return render(request, 'sendemail/sendemail.html', context={'form': form})
    

