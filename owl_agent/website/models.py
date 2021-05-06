from django import forms
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class User_Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_profile_url(self):
        return "/profile/{}/".format(self.user.username)

    def __str__(self):
        return self.user.username


class Company_Profile(User_Profile):
    image = models.ImageField(upload_to='company_image', null=True, blank=True, default='company_image/default.png')
    company_name = models.CharField(max_length=100)
    tax_id = models.IntegerField()
    website = models.CharField(max_length=100)
    foundation_year = models.IntegerField()


class Job_Seeker_Profile(User_Profile):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    carrier_list = models.CharField(max_length=2000)
    portfolio_link = models.CharField(max_length=100)
    image = models.ImageField(upload_to='job_seeker_image', null=True, blank=True,
                              default='job_seeker_image/default.png')


class CV(models.Model):
    name = models.CharField(max_length=20)
    cv_img = models.ImageField(upload_to='cv_image', null=True, blank=True, default='cv_img/default')
    almater = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    graduation_date = models.DateField()
    internships = models.TextField(max_length=2000)
    gpa = models.DecimalField(max_digits=20, decimal_places=2)
    experience_field = models.TextField(max_length=500)
    extras = models.TextField(max_length=1000)
    interests = models.TextField(max_length=1000)
    owner = models.ForeignKey(Job_Seeker_Profile, on_delete=models.CASCADE, related_name='%(class)s_owner')

    MILITARY_STATUS_CHOICES = [
        (1, 'Done'),
        (0, 'Not Done'),
    ]
    military_status = models.IntegerField(
        choices=MILITARY_STATUS_CHOICES,
        default=1,
    )

    LICENCES_STATUS_CHOICES = [
        (1, 'Have'),
        (0, 'Have Not'),
    ]
    licences_status = models.IntegerField(
        choices=LICENCES_STATUS_CHOICES,
        default=1,
    )

    def __str__(self):
        return self.name


class Job_Offer(models.Model):
    CATEGORIES = (
        ('design', 'Design & Creative'),
        ('design_development', 'Design & Development'),
        ('sales_marketing', "Sales & Marketing"),
        ('mobile_app', "Mobile Application"),
        ('construction', "Construction"),
        ("it", "Information Technology"),
        ("real_estate", "Real Estate"),
        ("content_writer", "Content Writer")
    )

    TYPE = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("intern", "Internship"),
        ("remote", "Remote")
    )

    EXPERIENCE = (
        ("0_years", "No experience"),
        ("1_2_years", "1-2 years"),
        ("2_3_years", "2-3 years"),
        ("3_6_years", "3-6 years"),
        ("6_more_years", "6-more years")
    )

    LOCATION = (
        ("istanbul", "Istanbul"),
        ("ankara", "Ankara"),
        ("izmir", "Izmir"),
        ("bursa", "Bursa")
    )

    categories = models.CharField(max_length=25, choices=CATEGORIES)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    required_skills = models.CharField(max_length=10000, blank=True)
    education = models.CharField(max_length=10000, blank=True)
    start_date = models.DateField(blank=True)
    post_date = models.DateField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=25, blank=True, choices=TYPE)
    location = models.CharField(max_length=500, choices=LOCATION)
    work_level = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=100, blank=True, choices=EXPERIENCE)
    salary = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company_Profile, on_delete=models.CASCADE, related_name='%(class)s_company')


# KBR:EKLEDİ
class Application(models.Model):
    applicant = models.ForeignKey(Job_Seeker_Profile, on_delete=models.CASCADE, related_name='%(class)s_applicant',
                                  default="")
    employer = models.ForeignKey(Company_Profile, on_delete=models.CASCADE, related_name='%(class)s_employer',
                                 default="")
    job_offer = models.ForeignKey(Job_Offer, on_delete=models.CASCADE, related_name='%(class)s_job_offer',
                                  default="")
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='%(class)s_cv', default="")
    file = models.FileField(null=True)

## Django have some notification system , we can add Notification Model when we get there.
