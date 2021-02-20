from django.shortcuts import render,redirect
from .models import CustomUser,Feeds,Like,Dislike,Comments,Follow
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse


# Create your views here.

def follow(request,id):
    usr2 = CustomUser.objects.get(pk = id)
    follo = Follow()
    follo.user = request.user
    follo.following = usr2.pk
    follo.save()
    if Follow.objects.filter(user=request.user, following=usr2.pk).exists():
        msg = 1
    else: 
        msg = 2
    return render(request,'single.html', {'usr3': usr2, 'msg': msg})

def unfollow(request,id):
    usr2 = CustomUser.objects.get(pk = id)
    Follow.objects.filter(user=request.user, following=usr2.pk).delete()
    if Follow.objects.filter(user=request.user, following=usr2.pk).exists():
        msg = 1
    else: 
        msg = 2
    return render(request,'single.html', {'usr3': usr2, 'msg': msg})

def single(request,id):
    usr2 = CustomUser.objects.get(pk = id)
    if Follow.objects.filter(user=request.user, following=usr2.pk).exists():
        msg = 1
    else: 
        msg = 2

    followers=Follow.objects.filter(following=usr2.pk).count() #follower
    following =Follow.objects.filter(user=usr2.pk).count() #following

    return render(request,'single.html', {'usr3': usr2, 'msg': msg , 'follower1':followers, 'following':following})

def userProfile(request):
    if 'q' in request.GET:
        q=request.GET['q']
        userlist1=CustomUser.objects.filter(first_name__icontains=q)
    else:
        userlist1 = CustomUser.objects.all()
    return render(request,'userProfile.html',{'userlist':userlist1})


def like(request, pk):
    if Like.objects.filter(user1=request.user.pk, feeds1=pk).exists(): # check user alredy liked or not
        pass
    else:                                                       #add like
        like = Like()
        like.user1 = request.user
        like.feeds1 = Feeds.objects.get(pk=pk)
        like.save()
    if Dislike.objects.filter(user1=request.user.pk, feeds1=pk).exists():   # check user already dislike the post
        Dislike.objects.filter(user1=request.user.pk, feeds1=pk).delete()   # if disliked remove dislike
    likecount = Like.objects.filter(feeds1=pk).count()# get likes count
    dislikecount = Dislike.objects.filter(feeds1=pk).count()# get dislike count
    feedDet = Feeds.objects.get(pk=pk)
    return render(request,'feedDetails.html', {'feedDet1': feedDet, 'likecount': likecount,'dislikecount': dislikecount })

def dislike(request, pk):
    if Dislike.objects.filter(user1=request.user.pk, feeds1=pk).exists(): # check user alredy disliked or not
        pass
    else:                                                    #add dislike
        dislike = Dislike()
        dislike.user1 = request.user
        dislike.feeds1 = Feeds.objects.get(pk=pk)
        dislike.save()
    if Like.objects.filter(user1=request.user.pk, feeds1=pk).exists():      # check user alreasy like the post
        Like.objects.filter(user1=request.user.pk, feeds1=pk).delete()      # if liked remove like
    
    likecount = Like.objects.filter(feeds1=pk).count() # get likes count
    dislikecount = Dislike.objects.filter(feeds1=pk).count()# get dislike count
    feedDet = Feeds.objects.get(pk=pk)
    return render(request,'feedDetails.html', {'feedDet1': feedDet, 'likecount': likecount,'dislikecount': dislikecount })




def feedDetails(request,id):
    if request.method == 'POST':
        print("post")
        description = request.POST.get('comment')
        print(description)
        date = datetime.now()
        user = request.user
        feed = Comments()
        feed.description = description
        feed.date = date
        feed.user = user
        feed.save()
    feed1 = Comments.objects.all().order_by('-date')
    usr = CustomUser.objects.all()
   # return render(request, 'home.html', {'feed': feed1, 'usr': usr})
    likecount = Like.objects.filter(feeds1=id).count() # get likes count
    dislikecount = Dislike.objects.filter(feeds1=id).count() # get dislike count
    feedDet = Feeds.objects.get(pk = id)
    return render(request,'feedDetails.html', { 'feed': feed1, 'usr': usr,  'feedDet1': feedDet, 'likecount': likecount,'dislikecount': dislikecount })



def home(request):
    if request.method == 'POST':
        print("post")
        description = request.POST.get('feed')
        print(description)
        date = datetime.now()
        user = request.user
        feed = Feeds()
        feed.description = description
        feed.date = date
        feed.user = user
        feed.save()
    feed1 = Feeds.objects.all().order_by('-date')
    
    follo = Follow.objects.filter(user=request.user)
    following_count = Follow.objects.filter(user=request.user).count()
    followers_count  = Follow.objects.filter(following=request.user.pk).count()
    return render(request, 'home.html', {'feed': feed1,  'follo': follo,
                                        'following_count': following_count, 'followers_count': followers_count})
    

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
               user = CustomUser.objects.create_user(username=username,dob=dob, password=password1, email=email,first_name=first_name,last_name=last_name)
               user.save();
               print('user created')
               
                

        else:
            messages.info(request,'password not matching..')    
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')


