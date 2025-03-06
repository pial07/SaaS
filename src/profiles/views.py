from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User=get_user_model

@login_required
def profile_view(request, username=None, *args , **kwargs):
    user=request.user
    profile_user_obj=User.objects.get(username=username)
    return HttpResponse(f"Hello {username}-{profile_user_obj.id}")