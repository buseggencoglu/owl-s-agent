from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.role_choose, name='register'),
    path('register_job_seeker/', views.register_Job_Seeker, name='register_job_seeker'),
    path('register_company/', views.register_Company, name='register_company'),
    path('sent/', views.activation_sent_view, name="sent"),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('job-details/', views.job_details_view, name='job-details'),
    path('job-listing/', views.job_listing_view, name='job-listing'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/single/', views.single_blog_view, name='single-blog'),
    path('elements/', views.elements_view, name='elements'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path ('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:pk>', views.approve_companies, name='company_approve'),
    path('dashboard/reject/<int:pk>', views.reject_companies, name='company_reject')
]
