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
    image = models.ImageField(upload_to='job_seeker_image', null=True, blank=True, default='job_seeker_image/default')



class CV(models.Model):
    almater = models.CharField(max_length=100)
    graduation_date = models.DateField()
    internships = models.CharField(max_length=2000)
    gpa = models.DecimalField(max_digits=20, decimal_places=2)
    experience_field = models.CharField(max_length=500)
    extras = models.CharField(max_length=1000)
    interests = models.CharField(max_length=1000)
    owner = models.ForeignKey(Job_Seeker_Profile, on_delete=models.CASCADE, related_name='%(class)s_owner')


class Job_Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=500)
    work_level = models.CharField(max_length=100)
    is_experience = models.BooleanField()
    quota = models.IntegerField()


class Application(models.Model):
    applicant = models.ForeignKey(Job_Seeker_Profile, on_delete=models.CASCADE, related_name='%(class)s_applicant')
    employer = models.ForeignKey(Company_Profile, on_delete=models.CASCADE, related_name='%(class)s_employer')
    job_offer = models.ForeignKey(Job_Offer, on_delete=models.CASCADE, related_name='%(class)s_job_offer')

## Django have some notification system , we can add Notification Model when we get there.
