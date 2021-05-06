from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .models import Company_Profile, Job_Seeker_Profile, CV, Application

User = get_user_model()

USER_TYPES = (
    ('job_seeker', 'Job_Seeker'),
    ('company', 'Company'),
)


class RoleChooseForm(forms.Form):
    type = forms.ChoiceField(choices=USER_TYPES)


class Job_Seeker_RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Name', widget=forms.TextInput)
    surname = forms.CharField(max_length=100, help_text='Surname', widget=forms.TextInput)
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    carrier_list = forms.CharField(max_length=2000, help_text='Carrier List', widget=forms.TextInput)
    portfolio_link = forms.CharField(max_length=100, help_text='Portfolio Link', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username', 'name', 'surname', 'password1', 'password2')


class Company_RegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, help_text='Company Name', widget=forms.TextInput)
    tax_id = forms.IntegerField()
    website = forms.CharField(max_length=100, help_text='Website', widget=forms.TextInput)
    foundation_year = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'company_name', 'password1', 'password2')


class EditCompanyProfileForm(forms.Form):
    company_name = forms.CharField(max_length=100, widget=forms.TextInput)
    foundation_year = forms.IntegerField()
    tax_id = forms.IntegerField()
    website = forms.CharField(max_length=100, widget=forms.TextInput)
    email = forms.EmailField(max_length=150, widget=forms.EmailInput)

    class Meta:
        model = Company_Profile
        fields = ('company_name', 'email', 'foundation_year', 'tax_id', 'website')


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = [
            'name',
            'cv_img',
            'address',
            'military_status',
            'licences_status',
            'almater',
            'graduation_date',
            'internships',
            'gpa',
            'experience_field',
            'extras',
            'interests'
        ]
        widgets = {
            'graduation_date': forms.DateInput(attrs={'class': 'form-control',
                                                      'type': 'date'}),
        }


# KBR:EKLEDİ
class JobApplyForm(forms.ModelForm):
    owner = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, job_seeker, **kwargs):
        super(JobApplyForm, self).__init__(*args, **kwargs)
        self.fields['cv'].queryset = CV.objects.filter(owner=job_seeker)

        self.fields['cv'].required = False
        self.fields['file'].required = False

    class Meta:
        model = Application
        fields = 'cv', 'file', 'owner'
        labels = {
            "file": "CV (pdf format)"
        }
