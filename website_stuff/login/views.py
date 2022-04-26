from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from test1 import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . tokens import generate_token
from .models import *

# Create your views here. 
def home(request):
    return render(request, "login/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to ATG Task 3 Project"
        message = "Hello " + myuser.first_name + "!! \n" + "Thank you for visiting the website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nSaransh Tiwari"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ ATG Task 3"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "login/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "login/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "login/signin.html")

@login_required(login_url='home')
def state(request):
    temp=[]
    for x in States.objects.all().values_list():
        temp.append(x[0])
    return render(request, 'login/state.html', {'states': temp})


@login_required(login_url='home')
def category(request):
    
    temp=[]
    for x in JobTypes1.objects.all().values_list():
        temp.append(x[0])
    request.session['fav_color'] = request.GET.get('state')
    #print(statename)
    return render(request, 'login/category.html', {'categories': temp})
    

@login_required(login_url='home')
def subcategory(request):
    temp=[]

    category=request.GET.get('category')
    for x in JobTypes2.objects.all().values_list():
        if (x[1] == category): temp.append(x[0])
    return render(request, 'login/subcategory.html', {'subcategories': temp})
@login_required(login_url='home')
def job(request):
    temp=[]
    subcategory=request.GET.get('subcategory')
    print(request.session['fav_color'])
    for x in Jobs.objects.all().values_list():
        print(request.session['fav_color'] in x[3]) 
        if (x[4] == subcategory and request.session['fav_color'] in x[3]): 
            temp.append(x[:4])
    
    return render(request, 'login/job.html', {'jobs': temp})


@login_required(login_url='home')
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

