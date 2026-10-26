from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from .forms import  ProfileUpdateForm, RegisterForm
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
           activation_link =f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}/"
           
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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:

        
        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            Profile.objects.get_or_create(user=user)

            messages.success(
                request,
                "Your account has been activated successfully."
            )

            login(request, user)
            return redirect('dashboard')
            

        else:
            messages.error(request, "Activation link is invalid!")
            return redirect('register')

    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')
  
def login_view(request):
    if request.method =="POST":
        form =AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user =form.get_user()
            login(request,user)
            return redirect('dashboard')

    else:
        form =AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

@login_required
def dashboard_view(request):
    profile = request.user.profile

    return render(
        request,
        'accounts/dashboard.html',
        {'profile': profile}
    )

@login_required
def update_profile(request):
   
    profile = request.user.profile

    if request.method == "POST":
        form =ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect ("dashboard")
    else:
        form = ProfileUpdateForm (instance=profile)
    return render (request, "accounts/update_profile.html", {
        "form": form,
        "profile": profile
    })

def logout_view(request):
    logout(request)
    return redirect("login")








  




