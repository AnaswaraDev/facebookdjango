from django.shortcuts import render,redirect
from .models import CustomUser,Feeds,Like,Dislike
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse


# Create your views here.
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
    likecount = Like.objects.filter(feeds1=id).count() # get likes count
    dislikecount = Dislike.objects.filter(feeds1=id).count() # get dislike count
    feedDet = Feeds.objects.get(pk = id)
    return render(request,'feedDetails.html', {'feedDet1': feedDet, 'likecount': likecount,'dislikecount': dislikecount })



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
    usr = CustomUser.objects.all()
    return render(request, 'home.html', {'feed': feed1, 'usr': usr})
    

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


