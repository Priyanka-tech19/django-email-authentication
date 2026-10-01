from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from django.conf import settings 
from .tokens import email_verification_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding  import force_bytes,force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfilePicForm, ProfileUpdateForm
from .models import Profile



def register_view(request):
    if request.method =='POST': 
        form = RegisterForm(request.POST)
        if form.is_valid():
           user=form.save(commit= False)
           user.is_active =False
           user.save()

           uid= urlsafe_base64_encode(force_bytes(user.pk))
           token =email_verification_token.make_token(user)
           activation_link =f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}"
           
           send_mail(
            'verify your mail',
            f'click the link below to verify your account:\n\n{activation_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
           )

           return HttpResponse("Please check your mail to verify your account.")
          
        else:
            print("Form.errors:", form.errors)
            error ="Form is invalid"
          
            
          
    else:
        form =RegisterForm()
    return render (request,'accounts/register.html',{'form':form})
  

def login_view(request):
    if request.method =="POST":
        form =AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user =form.get_user()
            login(request,user)
            return redirect('dashboard')

    else:
        form =AuthenticationForm()
    return render(request, 'Accounts/login.html', {'form':form})



def logout_view(request):
    logout(request)
    return redirect("login")



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except:

        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()

        Profile.objects.get_or_create(user=user)
        login(request,user)
        messages.success(request, "Your account has been verified successfully. Please upload your profile picture.")
        return redirect('upload_profile_pic')
    else:
        return HttpResponse("Activation link is invalid!")
   
@login_required
def dashboard_view(request):
    profile = request.user.profile
    # when user uploads new photo
    if request.method == 'POST':
        form =ProfilePicForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    # when user simply opens dashboard
    else:
        form =ProfilePicForm(instance=profile)

    context = {
        'form' :form,
        'profile': profile
    }
    return render (request, 'accounts/dashboard.html', context)


@login_required
def upload_profile_pic(request):

    # Auto create profile if missing
    profile, created = Profile.objects.get_or_create(user=request.user)
   

    if request.method == 'POST':
        if "profile_pic" in request.FILES:
            profile.profile_pic =request.FILES["profile_pic"]
            profile.save()
            messages.success(request,"Profile picture uploaded successfully!")
            return redirect("dashboard")
    return render (request,"accounts/upload_profile_pic.html",{"profile":profile})


@ login_required
def update_profile(request):
    profile, created =Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form =ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect ("dashboard")
    else:
        form = ProfileUpdateForm (instance=profile)
    return render (request, "accounts/update_profile.html", {
        "form": form,
        "profile": profile
    })




  




