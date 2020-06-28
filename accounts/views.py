from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.
def register(request):

    if request.method == 'POST':
        firstname= request.POST['first_name']
        lastname= request.POST['last_name']
        username= request.POST['username']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username):
                messages.info(request, 'Username Taken')
                print('username taked')
                return redirect('register')
            elif User.objects.filter(email=email):
                messages.info(request, 'email Taken')
                print('email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,password = password1, email=email, first_name=firstname,last_name=lastname)
                user.save()
                print ("user created")
                return redirect('login')
        else:
            messages.info(request, 'password not matching')
            print("password not matching")
            return redirect('register')
        return redirect('/')


    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        messages.info(request,'post')
        username = request.POST['username']
        password = request.POST['password']

        user= auth.authenticate(username=username,password=password)

        if user is not None:
            messages.info(request,'valid credentials')
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')


    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')