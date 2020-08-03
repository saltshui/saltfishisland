from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notifications.signals import notify
from users.models import User
from blog.models import Post
from .forms import CommentForm
from .models import Comment
from django.http import Http404
from django.contrib import messages


# 文章评论
@login_required(login_url='/users/basiclogin/')
def post_comment(request, article_id, parent_comment_id=None):
    #如果没有对应文章返回404
    article = get_object_or_404(Post, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #处理表单信息
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            
            #二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                #若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                #被回复人
                new_comment.reply_to = parent_comment.user
                #更新数据库
                new_comment.save()
                #向跟节点被回复人(非被回复人/管理)发送通知
                if not parent_comment.get_root().user.is_superuser: 
                    if request.user!=parent_comment.get_root().user and parent_comment.get_root().user!=parent_comment.user: 
                        notify.send(
                            request.user,
                            recipient=parent_comment.get_root().user,
                            verb='回复了你',
                            target=article,
                            action_object=new_comment,
                        )
                #向被回复人(非管理)发送通知
                if not parent_comment.user.is_superuser: 
                    if request.user!=parent_comment.user: 
                        notify.send(
                            request.user,
                            recipient=parent_comment.user,
                            verb='回复了你',
                            target=article,
                            action_object=new_comment,
                        )
                #向管理员发送通知
                if not request.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
    
                return HttpResponse('200 OK') 
            #更新数据库
            new_comment.save()

            #向管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )
            #回到文章界面
            messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
    
            return redirect(article)
        else:
            messages.add_message(request, messages.ERROR, '评论发表失败！请修改后重新提交。', extra_tags='danger')
            return redirect(article)    
            
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    #搞事就恰404
    else:
        raise Http404
