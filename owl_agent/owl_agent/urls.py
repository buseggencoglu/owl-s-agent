from django.contrib import admin
from django.urls import path

from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('job-details/', views.job_details_view, name='job-details'),
    path('job-listing/', views.job_listing_view, name='job-listing'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/single/', views.single_blog_view, name='single-blog'),
    path('elements/', views.elements_view, name='elements'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
