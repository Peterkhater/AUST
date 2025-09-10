from django.shortcuts import redirect
from django.contrib import messages

def farmer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'farmer':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You must be a farmer to access this page.")
            return redirect("home_page")  
    return wrapper
