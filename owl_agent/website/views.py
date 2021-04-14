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


def admin_dashboard_list(request):
   querySet = Company_Profile.objects.all()
   listing_jobseeker = Job_Seeker_Profile.objects.all()

   return render(request,"website/List.html",{"querySet": querySet, "listing_jobseeker": listing_jobseeker,},)

def admin_delete_companies(request,pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.delete()

    return HttpResponseRedirect('/dashboardList')


def admin_delete_jobseeker(request,pk):
    company = Job_Seeker_Profile.objects.get(id=pk)
    company.user.delete()

    return HttpResponseRedirect('/dashboardList')









def approve_companies(request,pk):
    company = Company_Profile.objects.get(id=pk)
    company.user.is_active = True
    company.user.save()

    return HttpResponseRedirect('/dashboard')

def reject_companies(request,pk):
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
        form = Job_Seeker_RegisterForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            # if (date.today() - form.cleaned_data['birthDate']) < timedelta(days=18 * 365):
            #     return render(request, template, {
            #         'form': form,
            #         'error_message': 'Age should be greater than 18.'
            #     })
            if Job_Seeker_Profile.objects.filter(portfolio_link=form.cleaned_data['portfolio_link']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'This portfolio link already exists.'
                })

            user = form.save()
            Job_Seeker_Profile.objects.create(user=user, name=form.cleaned_data['name'],
                                              surname=form.cleaned_data['surname'],
                                              birth_date=form.cleaned_data['birth_date'],
                                              carrier_list=form.cleaned_data['carrier_list'],
                                              portfolio_link=form.cleaned_data['portfolio_link'])
            user.is_active = True
            user.save()

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
        form = Company_RegisterForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            if (form.cleaned_data['foundation_year']) >= date.today():
                return render(request, template, {
                    'form': form,
                    'error_message': 'The foundation year cant be in future'
                })
            if Company_Profile.objects.filter(tax_id=form.cleaned_data['tax_id']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'This tax id already exists.'
                })

            user = form.save()
            Company_Profile.objects.create(user=user, company_name=form.cleaned_data['company_name'],
                                           tax_id=form.cleaned_data['tax_id'],
                                           website=form.cleaned_data['website'],
                                           foundation_year=form.cleaned_data['foundation_year'])
            user.is_active = False
            user.save()

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
