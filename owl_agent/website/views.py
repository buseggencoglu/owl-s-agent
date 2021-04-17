import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import Job_Seeker_RegisterForm, RoleChooseForm, Company_RegisterForm
from .models import Job_Seeker_Profile, Company_Profile
from datetime import date
from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)


# Create your views here.
# @login_required(login_url='login')
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


def admin_dashboard(request):
    context = {}
    user = request.user

    context["companies"] = Company_Profile.objects.filter(user__is_active=False)

    return render(request, 'website/dashboard.html', context)


def approve_companies(request, pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.is_active = True
    company.user.save()

    return HttpResponseRedirect('/dashboard')


def reject_companies(request, pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.delete()

    return HttpResponseRedirect('/dashboard')


def role_choose(request):
    template = 'website/role_choose.html'

    if request.method == "POST":
        form = RoleChooseForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type'] == 'job_seeker':
                return HttpResponseRedirect('/register_job_seeker')
            else:
                return HttpResponseRedirect('/register_company')

        return redirect('sent')
    else:
        form = RoleChooseForm()
    return render(request, template, {"form": form})


def register_Job_Seeker(request):
    # if this is a POST request we need to process the form data
    template = 'website/register_Job_Seeker.html'

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST['email']
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        birthdate_text = request.POST.get('foundation_year')
        birthdate = datetime.datetime.strptime(birthdate_text, '%Y-%m-%d')

        if password1 != password2:
            messages.error(request, 'Two password does not match.')
            return redirect('register_job_seeker')
        if len(password1) < 8:
            messages.error(request, 'Password should have minimum 8 charecters.')
            return redirect('register_job_seeker')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            messages.error(request, 'This email already using.')
            return redirect('register_job_seeker')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken..')
            return redirect('register_job_seeker')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password1)

        job_seeker_profile = Job_Seeker_Profile.objects.create(user=user, name=first_name,
                                                               surname=surname,
                                                               birth_date=birthdate)

        user.save()
        job_seeker_profile.save()

        # Login the user
        login(request, user)
        return redirect('sent')

    else:
        form = Job_Seeker_RegisterForm()
    return render(request, template, {"form": form})


def register_Company(request):
    # if this is a POST request we need to process the form data
    template = 'website/register_Company.html'

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST['email']
        company_name = request.POST.get('company')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        tax_id = request.POST.get('company_tax')
        website = request.POST.get('website')
        foundation_year = request.POST.get('foundation_year')

        if password1 != password2:
            messages.error(request, 'Two password does not match.')
            return redirect('register_company')
        if len(password1) <= 8:
            messages.error(request, 'Password should have minimum 8 charecters.')
            return redirect('register_company')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            messages.error(request, 'This email already using.')
            return redirect('register_company')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken..')
            return redirect('register_company')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password1)

        company_profile = Company_Profile.objects.create(user=user, company_name=company_name,
                                                         tax_id=tax_id,
                                                         website=website,
                                                         foundation_year=foundation_year)
        user.is_active = False
        user.save()
        company_profile.save()

        return redirect('sent')

    else:
        form = Company_RegisterForm()
    return render(request, template, {"form": form})


def activation_sent_view(request):
    return render(request, 'website/activation_sent.html')


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


def edit_profile_job_seeker(request):
    context = {}
    data = Job_Seeker_Profile.objects.get(user=request.user)
    context["data"] = data

    if request.method == "POST":
        data.name = request.POST["name"]
        data.surname = request.POST["surname"]
        data.carrier_list = request.POST["carrier_list"]
        data.portfolio_link = request.POST["portfolio_link"]
        data.gender = request.POST["gender"]

        if "image" in request.FILES:
            image = request.FILES["image"]
            data.image = image

        data.save()
        messages.success(request, "Profile updated successfully.")
    return render(request, 'website/edit_profile_job_seeker.html', context)
