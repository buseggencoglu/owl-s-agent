import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail.backends import console
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import Job_Seeker_RegisterForm, RoleChooseForm, Company_RegisterForm, EditCompanyProfileForm, CVForm
from .models import Job_Seeker_Profile, Company_Profile, Job_Offer, CV
from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import Job_Offer_Filter



from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)


def company_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        else:
            company_profile = Company_Profile.objects.get(user=user)
            if company_profile is not None:
                return function(request, *args, **kw)
            else:
                return redirect('home')

    return wrapper


# Create your views here.
# @login_required(login_url='login')
def home_view(request):
    job_offer_list = Job_Offer.objects.all()
    job_offer_filter = Job_Offer_Filter(request.GET, queryset=job_offer_list)
    return render(request, 'website/index.html',{'filter': job_offer_filter})


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    return render(request, 'website/contact.html')


def job_details_view(request):
    return render(request, 'website/job_details.html')


def job_listing_view(request):
    template = 'website/job_listing.html'
    context = {}

    if request.method == "POST":
        title = request.POST.get('title')
        location = request.POST['location']

        if location != "anywhere":
            job_offers = Job_Offer.objects.all().filter(title__contains=title,location=location)
        else:
            job_offers = Job_Offer.objects.all().filter(title__contains=title)
        print(job_offers.count())
        job_offers = create_paginator(request, job_offers)
        context = {'job_offer': job_offers}

        # console.log(title)
        # print(location)
    return render(request, template, context)


def blog_view(request):
    return render(request, 'website/blog.html')


def single_blog_view(request):
    return render(request, 'website/single-blog.html')


def elements_view(request):
    return render(request, 'website/elements.html')


@staff_member_required
def admin_dashboard(request):
    context = {}
    user = request.user

    context["companies"] = Company_Profile.objects.filter(user__is_active=False)

    return render(request, 'website/dashboard.html', context)


@staff_member_required
def approve_companies(request, pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.is_active = True
    company.user.save()

    return HttpResponseRedirect('/dashboard')


@staff_member_required
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


@company_required
def post_job(request):
    # if this is a POST request we need to process the form data
    template = 'website/post_job.html'

    if request.method == "POST":
        categories = request.POST.get('categories')
        title = request.POST.get('title')
        description = request.POST['description']
        required_skills = request.POST['required_skills']
        education = request.POST['education']
        location = request.POST['location']
        type = request.POST['type']
        experience = request.POST.get('experience')
        salary = request.POST['salary']
        start_date = request.POST['start_date']
        company = Company_Profile.objects.get(user=request.user)

        job_offer = Job_Offer.objects.create(categories=categories, title=title, description=description,
                                             required_skills=required_skills,
                                             education=education, location=location,
                                             type=type, salary=salary,
                                             experience=experience, start_date=start_date,
                                             company=company)
        job_offer.save()

        return redirect('job_sent')

    return render(request, template)


def activation_sent_view(request):
    return render(request, 'website/activation_sent.html')


def job_sent_view(request):
    return render(request, 'website/job_sent.html')


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


def add_cv(request, pk=None):
    owner = Job_Seeker_Profile.objects.get(user=request.user)
    data = request.POST or None
    instance = None
    if pk is not None:
        instance = CV.objects.get(pk=pk, owner=owner)

    form = CVForm(data, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            cv = form.save(commit=False)
            cv.owner = owner

            if "cv_img" in request.FILES:
                cv.cv_img = request.FILES["cv_img"]

            cv.save()
            return redirect(f'/job_seeker_profile/{request.user.id}')
    context = {
        'form': form,
        'pk': pk
    }
    return render(request, 'website/add_cv.html', context)


def delete_cv(request, pk):
    instance = CV.objects.get(pk=pk)
    instance.delete()
    return redirect(f'/job_seeker_profile/{request.user.id}')




def job_seeker_profile(request, pk):
    context = {'is_my_profile':pk==request.user.id}
    data = Job_Seeker_Profile.objects.get(user_id=pk)
    context["data"] = data

    cvs = CV.objects.filter(owner=data)
    context['cvs'] = cvs

    return render(request, 'website/job_seeker_profile.html', context)


def edit_profile_job_seeker(request,pk):
    context = {}
    data = Job_Seeker_Profile.objects.get(user=pk)
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
        return redirect('job_seeker_profile', pk=pk)
    else:
        return render(request, 'website/edit_profile_job_seeker.html', context)


def company_profile(request, pk):
    profile = Company_Profile.objects.get(user_id=pk)
    job_posts = Job_Offer.objects.filter(company=profile)
    print("****", job_posts)
    args = {'profile': profile, 'job_posts':job_posts}
    return render(request, 'website/company_profile.html', args)


def edit_profile_company(request, pk):
    template = 'website/edit_profile_company.html'
    company = Company_Profile.objects.filter(user=request.user)[0]


    if request.method == 'POST':
        image = request.FILES.get('image')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        foundation_year = request.POST.get('foundation_year')
        tax_id = request.POST.get('tax_id')
        website = request.POST.get('website')

        if Company_Profile.objects.filter(company_name=company_name).exclude(
                company_name=company.company_name).exists():
            messages.error(request, 'This company name is already in use.')
            return redirect('edit_profile_company', pk=pk)

        if email and User.objects.filter(email=email).exclude(email=company.user.email).exists():
            messages.error(request, 'This email is already in use.')
            return redirect('edit_profile_company', pk=pk)

        if Company_Profile.objects.filter(tax_id=tax_id).exclude(
                tax_id=company.tax_id).exists():
            messages.error(request, 'This tax id is already in use.')
            return redirect('edit_profile_company', pk=pk)

        if image is None:
            image = company.image

        user = User.objects.filter(pk=pk)
        user.update(email=email)

        company_p = Company_Profile.objects.get(user_id=pk)
        company_p.image = image
        company_p.company_name = company_name
        company_p.foundation_year = foundation_year
        company_p.tax_id = tax_id
        company_p.website = website
        company_p.save()

        return redirect('company_profile', pk=pk)
    else:
        form = EditCompanyProfileForm()
        args = {'form': form, 'company': company}
        return render(request, template, args)


def admin_dashboard_list(request):
    querySet = Company_Profile.objects.all().order_by()
    querySet = create_paginator(request, querySet)
    listing_jobseeker = Job_Seeker_Profile.objects.all().order_by()
    listing_jobseeker = create_paginator(request, listing_jobseeker)

    return render(request, 'website/listing.html', {'querySet': querySet, 'listing_jobseeker': listing_jobseeker})

def admin_dashboard_job_list(request):
    querySet = Job_Offer.objects.all().order_by()
    querySet = create_paginator(request, querySet)

    return render(request, 'website/admin_job_listing.html', {'querySet': querySet, 'listing_job_offer': querySet})


def admin_delete_companies(request, pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.delete()

    return HttpResponseRedirect('/dashboardList')


def admin_delete_jobseeker(request, pk):
    company = Job_Seeker_Profile.objects.get(id=pk)
    company.user.delete()

    return HttpResponseRedirect('/dashboardList')


def create_paginator(request, list):
    page = request.GET.get('page', 1)
    paginator = Paginator(list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts

