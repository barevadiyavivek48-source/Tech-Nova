from django.shortcuts import render, redirect
from functools import wraps
from myapp.models import User as AppUser
from .models import VendorProfile
from django.contrib import messages
# Import Category from vendor app
from .models import Category, Product
from myapp.models import Order


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_session_user(request):
    email = request.session.get('email')
    if not email:
        return None
    try:
        return AppUser.objects.get(email=email)
    except AppUser.DoesNotExist:
        request.session.pop('email', None)
        return None

# Vendor add category view


@login_required
def vendor_add_category(request):
    user = _get_session_user(request)
    if not user or user.role != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('/')
    context = {'user_name': user.name, 'user_email': user.email}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        if not name:
            messages.error(request, 'Category name is required.')
        else:
            Category.objects.create(
                name=name, description=description, image=image)
            messages.success(request, 'Category added successfully!')
            return redirect('vendor:vendor_dashboard')
    return render(request, 'vendor_add_category.html', context)

# Vendor add product view


@login_required
def vendor_add_product(request):
    user = _get_session_user(request)
    if not user or user.role != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('/')
    categories = Category.objects.all()
    context = {'categories': categories,
               'user_name': user.name, 'user_email': user.email}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        quantity = request.POST.get('stock', '').strip()
        category_id = request.POST.get('category', '')
        image = request.FILES.get('image')
        category = Category.objects.filter(id=category_id).first()
        profile = VendorProfile.objects.filter(user=user).first()
        if not name or not price or not quantity or not category or not profile:
            messages.error(request, 'All fields are required.')
        else:
            Product.objects.create(
                vendor=profile,
                category=category,
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                image=image
            )
            messages.success(request, 'Product added successfully!')
            return redirect('vendor:vendor_dashboard')
    return render(request, 'vendor_add_product.html', context)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_session_user(request):
    email = request.session.get('email')
    if not email:
        return None
    try:
        return AppUser.objects.get(email=email)
    except AppUser.DoesNotExist:
        request.session.pop('email', None)
        return None


@login_required
def vendor_account(request):
    user = _get_session_user(request)
    if not user or user.role != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('/')
    profile, _ = VendorProfile.objects.get_or_create(user=user)
    context = {'profile': profile}
    context['user_name'] = user.name
    context['user_email'] = user.email
    if request.method == 'POST':
        profile.shop_name = request.POST.get('shop_name', profile.shop_name)
        profile.address = request.POST.get('address', profile.address)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.website = request.POST.get('website', profile.website)
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('vendor:vendor_dashboard')
    return render(request, 'vendor_account.html', context)


@login_required
def vendor_grid(request):
    user = _get_session_user(request)
    if not user or user.role != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('/')
    profiles = VendorProfile.objects.select_related('user').all()
    context = {
        'user_name': user.name,
        'user_email': user.email,
        'profiles': profiles,
    }
    return render(request, 'vendor_grid.html', context)


@login_required
def vendor_dashboard(request):
    user = _get_session_user(request)
    if not user or user.role != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('/')
    profile = None
    try:
        profile = VendorProfile.objects.get(user=user)
    except VendorProfile.DoesNotExist:
        pass
    # Get all categories and products for this vendor
    categories = Category.objects.all()
    products = Product.objects.filter(vendor=profile) if profile else []

    # Get all orders containing this vendor's products
    orders = []
    if profile:
        all_orders = Order.objects.all().order_by('-created_at')
        for order in all_orders:
            for item in order.items_json:
                # Try to match product name and vendor
                prod = Product.objects.filter(
                    name=item.get('name', ''), vendor=profile).first()
                if prod:
                    orders.append({
                        'order': order,
                        'customer': order.uid,
                        'product': prod,
                        'item': item
                    })
    context = {
        'profile': profile,
        'user_name': user.name,
        'user_email': user.email,
        'categories': categories,
        'products': products,
        'orders': orders,
    }
    return render(request, 'vendor_dashboard.html', context)
