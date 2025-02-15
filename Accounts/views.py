from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .forms import RegistrationForm
from .models import *

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname  = form.cleaned_data['last_name']
            email     = form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_number']
            password  = form.cleaned_data['password']
            username  = email.split("@")[0]

            user = Account.objects.create_user(first_name = firstname, last_name = lastname, email = email, username = username, phone_number = phone_num, password = password)
            user.phone_number = phone_num
            user.save()

            # USER ACTIVATION EMAIL VERIFICATION
            current_site = get_current_site(request)
            mail_subject = "Activate account"
            mail_message = render_to_string('accounts/account_activation_email.html', {
                'user': user, # user is above mentioned user
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user)
                
            })
            to_email = email # user email address
            send_email = EmailMessage(mail_subject, mail_message, to = [to_email])
            send_email.send()

            return redirect('signin')

    else:
        form = RegistrationForm()
        
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        # Try authentication
        user_auth = authenticate(request, email=email, password=password)
        print(f"Authentication result: {user_auth}")

        if user_auth:
            login(request, user_auth)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'accounts/login.html')


@login_required(login_url = 'signin')
def signout(request):
    logout(request)
    return redirect('home')
