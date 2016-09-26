from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'index.html')


@login_required(login_url='/')
def home(request):
    return render_to_response(index)


def logout(request):
    auth_logout(request)
    return redirect('/')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
