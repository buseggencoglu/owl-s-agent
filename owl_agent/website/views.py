from django.shortcuts import render


# Create your views here.

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
