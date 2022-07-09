from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from . models import Product
from . forms import UserUpdation

@never_cache
def index(request):
    return render(request, "authentication/index.html")

@never_cache
@login_required(login_url='index')
def home(request):
    products = Product.objects.all()
    return render(request, "authentication/page.html",{'products':products})

@never_cache
def signup(request):

    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1==pass2:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()

            messages.success(request, "Your Account has been Successfully Created.")

            return redirect('signin')
        else:
            messages.error(request,'Please match sure your passwords match')
            return redirect('signup')

    return render(request, "authentication/signup.html")

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']

            user = authenticate(username=username, password=pass1)

            if user is not None:
                login(request, user)
                products = Product.objects.all()
                return render(request, "authentication/page.html",{'products':products})
            else:
                messages.error(request, "Wrong Username or Password!!!")
                return redirect('signin')

    return render(request, 'authentication/signin.html')

@never_cache
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('index')

@never_cache
@login_required(login_url='index')
@user_passes_test(lambda u: u.is_superuser)
def showadmin(request):
    allusers = User.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        allusers = User.objects.filter(username__icontains=q)

    return render(request,'authentication/admin.html',{'alluser':allusers})

@never_cache
@login_required(login_url='index')
def update(request,id):
    if request.method == "POST":
        pi = User.objects.get(pk=id)
        fm = UserUpdation(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('showadmin')
    else:
        pi = User.objects.get(pk=id)
        fm = UserUpdation(instance=pi)
    return render(request,'authentication/updateuser.html',{'form':fm})

@never_cache
def delete(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return redirect("showadmin")
