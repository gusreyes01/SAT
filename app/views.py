# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render_to_response('home/home.html', context_instance=RequestContext(request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            HttpResponse('')# Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
         HttpResponse('')
        
def logout_view(request):
    logout(request)
    # Redirect to a success page.