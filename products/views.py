from django.shortcuts import render
from openrouter_utils import get_ai_recommendation
from users.decorators import farmer_required
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.cache import cache
from rapidfuzz import fuzz

# def products(request):
#     # All products
#     products = Product.objects.all()
#     categories = Product.CATEGORY_CHOICES
#     product_count = products.count()

#     is_organic = request.GET.get('is_organic')
#     if is_organic:
#         products = products.filter(is_organic=True)

#     is_local_farm = request.GET.get('is_local_farm')
#     if is_local_farm:
#         products = products.filter(is_local_farm=True)

#     category = request.GET.get('category')
#     if category:
#         products = products.filter(category__iexact=category)

#     recommended_products = Product.objects.none()

#     if request.user.is_authenticated:
#         user_location = f"{request.user.governorate}/{request.user.city_village}"
#         print(user_location)
#         cache_key = f"nearby_villages_{request.user.id}"

#         nearby_villages_str = cache.get(cache_key)

#         if not nearby_villages_str:
#             nearby_villages_str = get_ai_recommendation(
#                 prompt=f"""
#                 You are an assistant that knows all villages in Lebanon and their geographical proximity. 
#                 The user's village is '{user_location}'.
                
#                 Please provide a list of the 10 villages that are **closest to the user's village**, based on real-world distance (like what Google Maps would suggest). 
#                 Return **only the village names**, as a comma-separated list, without any explanation.
#                 Make sure the village names are correctly spelled.
#                 """,
#                 system_message="You are a helpful recommendation engine providing nearby village recommendations.",
#                 temperature=0.5
#             )

#             # Cache the result for 24 hours
#             cache.set(cache_key, nearby_villages_str, timeout=86400)

#         nearby_villages = [v.strip() for v in nearby_villages_str.split(",") if v.strip()]
#         villages_to_search = [request.user.city_village] + nearby_villages

#         all_products = Product.objects.all()
#         recommended_products = []

#         for product in all_products:
#             for village in villages_to_search:
#                 if fuzz.ratio(product.farmer.city_village.lower(), village.lower()) > 80:
#                     recommended_products.append(product)
#                     break  
        
#         recommended_products = sorted(recommended_products, key=lambda x: x.created_at, reverse=True)[:20]

#     context = {
#         'products': products,
#         'product_count': product_count,
#         'categories': categories,
#         'recommended_products': recommended_products, 
#     }

#     if request.user.is_authenticated:
#         context = {
#         'products': products,
#         'product_count': product_count,
#         'categories': categories,
#         'recommended_products': recommended_products, 
#         'villages_to_search':villages_to_search
#         }
#     return render(request, 'products/products.html', context)


def products(request):
    # Base products queryset
    products = Product.objects.all()
    categories = Product.CATEGORY_CHOICES
    product_count = products.count()

    # Filters
    if request.GET.get('is_organic'):
        products = products.filter(is_organic=True)

    if request.GET.get('is_local_farm'):
        products = products.filter(is_local_farm=True)

    category = request.GET.get('category')
    if category:
        products = products.filter(category__iexact=category)

    recommended_products = Product.objects.none()
    villages_to_search = []

    if request.user.is_authenticated:
        user_location = f"{request.user.governorate}/{request.user.city_village}"
        cache_key = f"nearby_villages_{request.user.id}"

        nearby_villages_str = cache.get(cache_key)

        if not nearby_villages_str:
            try:
                nearby_villages_str = get_ai_recommendation(
                    prompt=f"""
                    You are an assistant that knows all villages in Lebanon and their geographical proximity. 
                    The user's village is '{user_location}'.
                    
                    Please provide a list of the 10 villages that are **closest to the user's village**, based on real-world distance (like what Google Maps would suggest). 
                    Return **only the village names**, as a comma-separated list, without any explanation.
                    Make sure the village names are correctly spelled.
                    """,
                    system_message="You are a helpful recommendation engine providing nearby village recommendations.",
                    temperature=0.5
                )
                cache.set(cache_key, nearby_villages_str, timeout=86400)  # Cache for 24 hours
            except Exception as e:
                print("AI recommendation error:", e)
                nearby_villages_str = ""

        nearby_villages = [v.strip() for v in nearby_villages_str.split(",") if v.strip()]
        villages_to_search = [request.user.city_village] + nearby_villages

        # Fuzzy matching to get recommended products
        recommended_products_list = []
        for product in Product.objects.select_related('farmer').all():
            for village in villages_to_search:
                if product.farmer.city_village and fuzz.ratio(product.farmer.city_village.lower(), village.lower()) > 80:
                    recommended_products_list.append(product)
                    break
        
        # Sort by creation date and limit to 20
        recommended_products = sorted(recommended_products_list, key=lambda x: x.created_at, reverse=True)[:20]
        print(villages_to_search)
    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories,
        'recommended_products': recommended_products,
        'villages_to_search': villages_to_search
    }

    return render(request, 'products/products.html', context)


@login_required
@farmer_required
def products_add(request):
    if request.method == "POST":
        
        name=request.POST.get("name")
        description=request.POST.get("description")
        category=request.POST.get("category")
        price=request.POST.get("price") or 0
        quantity=request.POST.get("quantity") or 0
        min_order=request.POST.get("min_order") or 0
        harvest_date=request.POST.get("harvestDate")
        pricing_model=request.POST.get("pricing_model")
        shelf_life=request.POST.get('shelf_life')
        shelf_life_type = request.POST.get('shelf_life_DAY_OR_WEEK')
        is_local_farm=request.POST.get("is_local_farm") == "true"
        is_non_gmo=request.POST.get("isNon_gmo") == "true"
        is_organic=request.POST.get("isOrganic") == "true"
        image1=request.FILES.get("image1")
        image2=request.FILES.get("image2")
        image3=request.FILES.get("image3")
        farmer=request.user
    
        if image1 and image2 and image3:
            Product.objects.create( name=name,
                                    description=description,
                                    category=category,
                                    price=price,
                                    quantity=quantity,
                                    harvest_date=harvest_date,
                                    unit=pricing_model,
                                    shelf_life=shelf_life,
                                    is_local_farm=is_local_farm,
                                    is_Non_GMO=is_non_gmo,
                                    is_organic=is_organic,
                                    image1=image1,
                                    image2=image2,
                                    image3=image3,
                                    shelf_life_type=shelf_life_type,
                                    min_order=min_order,
                                    farmer=farmer)
            print("product created")
    return render(request,'products/product_add.html',{})

