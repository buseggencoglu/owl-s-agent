from website.models import Company_Profile,Job_Seeker_Profile

def user_type(request):
    user = request.user
    if not user.is_anonymous:
        company = Company_Profile.objects.filter(user=user)
        job_seeker = Job_Seeker_Profile.objects.filter(user=user)
        user_type = 'admin'
        if len(company) > 0:
            user_type = 'company'
        elif len(job_seeker) > 0:
            user_type= 'job_seeker'
        return {
            'user': user,
            'user_type': user_type,
        }
    return {}
