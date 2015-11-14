from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'app/index.html')

@login_required
def guides(request):
    return render(request, 'app/guides.html')


def login_view(request):
    return render(request, 'app/login.html')


def dologin_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'app/index.html')
        else:
            # Return a 'disabled account' error message
            return render(request, 'app/login_error.html')
    else:
        # Return an 'invalid login' error message.
        return render(request, 'app/login_error.html')
