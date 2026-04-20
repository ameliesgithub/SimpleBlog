from django.contrib.auth.models import User

from blog.models import UserProfile


def create_user(username,password, first_name, last_name, email, github_url, linkedin_url):
    user = User(username=username, first_name=first_name, last_name=last_name, email=email)
    user.set_password(password)
    user.save()

    profile = UserProfile(user=user, github_url=github_url, linkedin_url=linkedin_url)
    profile.save()