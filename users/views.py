from django.shortcuts import render
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile = get_object_or_404(Profile,user=request.user)
    return render(request,'users/profile.html',{'data':profile})