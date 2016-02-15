from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Create your views here.

# go to: https://docs.djangoproject.com/en/1.9/topics/auth/default/
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            print "disabled account"
    else:
        # Return an 'invalid login' error message.
        print "invalid login"


def logout_view(request):
    logout(request)
