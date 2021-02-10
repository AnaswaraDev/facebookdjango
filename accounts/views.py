from django.shortcuts import render,redirect
from .models import CustomUser,Feeds
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse


# Create your views here.
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


