from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.


def blogHome(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)



def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comment = BlogComment.objects.filter(post=post ,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict ={}
    for reply in replies: 
        if reply.parent.sno not in replyDict.keys():
              replyDict[reply.parent.sno] = [reply]
        else:
         replyDict[reply.parent.sno].append(reply)

         
    contex = {"post":post,'comment':comment,'user':request.user,'replyDict': replyDict}
    print(request)
    return render (request,"blog/blogPost.html",contex)
    # return HttpResponse("this is post of blog you can write slug post {slug}".format(slug=slug))


def postComment(request):
    if request.method == 'POST':
            comment = request.POST.get('comment')
            user = request.user
            postSno = request.POST.get('postSno')
            post = Post.objects.get(sno=postSno)
            parentSno= request.POST.get('parentSno')
            if parentSno =="": 
                comment=BlogComment(comment= comment, user=user, post=post)
                
                messages.success(request, "Your comment has been posted successfully")
            else:
                 parent = BlogComment.objects.get(sno = parentSno)
                 comment=BlogComment(comment= comment, user=user, post=post,parent =parent)
                 messages.success(request, "Your reply has been posted successfully")
            comment.save()
                 


    return redirect(f"/blog/{post.slug}")


