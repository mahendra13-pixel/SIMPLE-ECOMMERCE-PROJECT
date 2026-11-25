from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser,Profile
import re
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from core.views import index
from .forms import ProfileForm

# Login — uses EMAIL field from your form
def register(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('fname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        street_address=request.POST.get('streetadress')
        username=request.POST.get('username')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        if password == password1:
            error=[]
            if CustomUser.objects.filter(username=username).exists():
                error.append('username already exist')
               
            if CustomUser.objects.filter(email=email).exists():
                error.append('email already exist')
            if CustomUser.objects.filter(phone=phone).exists():
                error.append('phone number already exist')

            if not re.search(r'[A-Z]',password):
                error.append('password must contain at least on upper case')
            if not re.search(r'\d',password):
                error.append('your password must contain at least digit')
            if not re.search(r'\W',password):
                error.append('your password must contain at least one special character')
            
            try:
                validate_password(password)
                if not error:

                    CustomUser.objects.create_user(first_name=fname,last_name=lname,email=email,phone=phone,street_address=street_address,username=username,password=password)
                    messages.success(request,'register successfully')
                    return redirect('register')
                else:
                    for i in error:
                        messages.error(request,i)
                    return redirect("register")
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,"password and confirm password doesn't match")
            return redirect('register')
        
    return render(request,'register.html')
def log_in(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        remember_me=request.POST.get('remember_me') #on for click and none for unclick
        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request,"username doesn't exist!!")
            return redirect('log_in')

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(1800)
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next',"") #/about/
            return redirect(next if next else index)
        else:
            messages.error(request,"invalid password")
            return redirect('log_in')
        
    next=request.GET.get('next','')
    return render(request,'login.html',{'next':next})

def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='login')
def profile_dashboard(request):
    return render(request,'profile/dashboard.html')

@login_required(login_url='login')
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)

    if request.method =="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    context={
        'form':form
    }
    return render(request,'profile/profile.html',context)
