from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
# Create your views here.


def index(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")

        else:
            messages.info(request,'invalid credentials')
            return redirect('index')

    else:
        return render(request,'index.html')

