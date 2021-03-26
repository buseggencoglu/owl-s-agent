from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    return render(request, 'website/contact.html')


def job_details_view(request):
    return render(request, 'website/job_details.html')


def job_listing_view(request):
    return render(request, 'website/job_listing.html')


def blog_view(request):
    return render(request, 'website/blog.html')


def single_blog_view(request):
    return render(request, 'website/single-blog.html')


def elements_view(request):
    return render(request, 'website/elements.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'website/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')
