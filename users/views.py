from django.shortcuts import render
from .models import Profile
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm
from products.models import Product

@login_required
def profile(request):
    profile = get_object_or_404(Profile,user=request.user)
    user_product = Product.objects.filter(farmer=request.user)
    products_count = user_product.count()
    return render(request,'users/profile.html',{'data':profile,'products':user_product,'products_count':products_count})





@login_required
def profile_update(request):
    prof = get_object_or_404(Profile,user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/profile_update.html', {'form': form,'profile_data':prof})