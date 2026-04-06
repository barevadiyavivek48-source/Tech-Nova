from reportlab.platypus import HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib import pagesizes
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
from django.shortcuts import redirect
from django.http import HttpResponse
from io import BytesIO
import json
from django.utils import timezone
from django.conf import settings
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from functools import wraps
import re
from myapp2.models import Category, Product
from django.db.models import Q
from .models import User as AppUser
from .models import *
from django.shortcuts import get_object_or_404
import razorpay

# Custom session-based login guard


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Custom session-based login guard


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Billing view


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Wishlist views


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# Vendor add category view


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# Create your views here.

def _get_session_user(request):
    """Get user from session if logged in"""
    if 'email' in request.session:
        try:
            return User.objects.get(email=request.session['email'])
        except User.DoesNotExist:
            return None
    return None


def _get_recommended_products(limit=6):
    """Prioritize electronics-like names for search recommendations."""
    keyword_query = (
        Q(name__icontains="phone")
        | Q(name__icontains="iphone")
        | Q(name__icontains="watch")
        | Q(name__icontains="smartwatch")
        | Q(name__icontains="headphone")
        | Q(name__icontains="earbud")
        | Q(name__icontains="airpod")
    )

    priority = list(Product.objects.filter(keyword_query).order_by("-id")[:limit])
    if len(priority) >= limit:
        return priority

    priority_ids = [item.id for item in priority]
    remaining = limit - len(priority)
    fallback = list(Product.objects.exclude(id__in=priority_ids).order_by("-id")[:remaining])
    return priority + fallback

def home(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    from myapp2.models import Category
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        # Get cart item count
        cart_count = Add_to_cart.objects.filter(uid=user).count()
        context['cart_count'] = cart_count
    else:
        context['cart_count'] = 0
    # Always show all vendor categories and products on homepage
    context['categories'] = Category.objects.all()
    from myapp2.models import Product
    # Get all products sorted by newest first
    context['products'] = Product.objects.all().order_by('-id')
    context['recommended_products'] = _get_recommended_products(6)
    context['selected_category'] = None
    return render(request, 'index.html', context)


def category_products(request, category_id):
    """View to display products filtered by category"""
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    
    from myapp2.models import Category, Product
    
    # Get the selected category
    category = get_object_or_404(Category, id=category_id)
    
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        # Get cart item count
        cart_count = Add_to_cart.objects.filter(uid=user).count()
        context['cart_count'] = cart_count
    else:
        context['cart_count'] = 0
    
    # Show all categories and filtered products
    context['categories'] = Category.objects.all()
    context['products'] = Product.objects.filter(category_id=category_id).order_by('-id')
    context['recommended_products'] = _get_recommended_products(6)
    context['selected_category'] = category
    
    return render(request, 'index.html', context)


def search_products(request):
    """View to handle product search"""
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    
    from myapp2.models import Category, Product
    
    # Get search query from GET parameter
    search_query = request.GET.get('q', '').strip()
    print(f"DEBUG: Search query received: '{search_query}'")  # Debug log
    
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        # Get cart item count
        cart_count = Add_to_cart.objects.filter(uid=user).count()
        context['cart_count'] = cart_count
    else:
        context['cart_count'] = 0
    
    # Show all categories
    context['categories'] = Category.objects.all()
    
    # Filter products by search query (search in name and description)
    if search_query and len(search_query) > 0:
        # Search with case-insensitive matching in name and description
        search_products_list = Product.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).order_by('-id').distinct()
        
        print(f"DEBUG: Found {search_products_list.count()} products for query '{search_query}'")  # Debug log
        
        context['products'] = search_products_list
        context['search_query'] = search_query
        context['search_results_count'] = search_products_list.count()
    else:
        # If no search query, show all products
        print("DEBUG: No search query, showing all products")  # Debug log
        context['products'] = Product.objects.all().order_by('-id')
        context['search_query'] = None
        context['search_results_count'] = Product.objects.count()
    
    context['recommended_products'] = _get_recommended_products(6)
    context['selected_category'] = None
    
    return render(request, 'index.html', context)


def search_dropdown_api(request):
    """AJAX API to get search results for dropdown"""
    from django.http import JsonResponse
    from myapp2.models import Product
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 1:
        # Return recommended products if no search query
        products = _get_recommended_products(6)
    else:
        # Search products by name, description, and category
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).order_by('-id').distinct()[:10]
    
    # Format response
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'image': product.image.url if product.image else '',
            'url': f'/product_details/{product.id}/',
            'price': str(product.price),
        })
    
    return JsonResponse({
        'results': results,
        'query': query,
    })


# ── Custom session-based login guard ─────────────────────────────────────────
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            messages.warning(
                request, 'Please login or register to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# Alias for login_required
login_required_custom = login_required


# ── Auth views ────────────────────────────────────────────────────────────────
def login_view(request):
    if 'email' in request.session:
        return redirect('index')
    try:
        if request.method == 'POST':
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if not email or not password:
                messages.error(request, 'Email and password are required.')
                return render(request, 'login.html')

            user = AppUser.objects.get(email=email)

            if user.password == password:
                request.session['email'] = user.email
                return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    except AppUser.DoesNotExist:
        messages.error(request, 'Email not found.')
        return render(request, 'login.html')


def register_view(request):
    if 'email' in request.session:
        return redirect('index')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'customer')
        shop_name = request.POST.get(
            'shop_name', '').strip() if role == 'vendor' else ''

        if not name or not email or not password or not role:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if role == 'vendor' and not shop_name:
            messages.error(request, 'Shop name is required for vendors.')
            return render(request, 'register.html')

        if AppUser.objects.filter(email=email).exists():
            messages.error(
                request, 'This email is already registered. Please log in.')
            return redirect('login')

        if len(password) < 8:
            messages.error(
                request, 'Password must be at least 8 characters long.')
            return render(request, 'register.html')

        if not re.search(r'[A-Z]', password):
            messages.error(
                request, 'Password must include an uppercase letter.')
            return render(request, 'register.html')

        if not re.search(r'[a-z]', password):
            messages.error(
                request, 'Password must include a lowercase letter.')
            return render(request, 'register.html')

        if not re.search(r'\d', password):
            messages.error(request, 'Password must include a number.')
            return render(request, 'register.html')

        if not re.search(r'[^A-Za-z0-9]', password):
            messages.error(request, 'Password must include a symbol.')
            return render(request, 'register.html')

        user = AppUser.objects.create(
            name=name,
            email=email,
            password=password,
            role=role
        )

        messages.success(
            request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    if 'email' in request.session:
        del request.session['email']
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def login_view(request):
    if 'email' in request.session:
        user = AppUser.objects.get(email=request.session['email'])
        if user.role == 'vendor':
            return redirect('vendor:vendor_dashboard')
        else:
            return redirect('index')
    try:
        if request.method == 'POST':
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if not email or not password:
                messages.error(request, 'Email and password are required.')
                return render(request, 'login.html')

            user = AppUser.objects.get(email=email)

            if user.password == password:
                request.session['email'] = user.email
                if user.role == 'vendor':
                    return redirect('vendor:vendor_dashboard')
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Invalid password.')
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    except AppUser.DoesNotExist:
        messages.error(request, 'Email not found.')
        return render(request, 'login.html')
    return render(request, 'checkout.html')


def contact(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    if request.method == "POST":
        Contact.objects.create(
            fname=request.POST.get('first_name'),
            lname=request.POST.get('last_name'),
            phone_no=request.POST.get('phone'),
            email=request.POST.get('email'),
            sub=request.POST.get('subject'),
            msg=request.POST.get('message'),
        )
        return redirect('contact')
    return render(request, 'contact.html', context)


def my_account(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
        # Fetch orders for the user
        orders = Order.objects.filter(uid=user).order_by('-created_at')
        # Convert created_at to local timezone for each order
        for order in orders:
            order.created_at = timezone.localtime(order.created_at)
        context['orders'] = orders
        # Fetch addresses for the user
        context['addresses'] = Address.objects.filter(uid=user)
    else:
        context['cart_count'] = 0
        context['orders'] = []
        context['addresses'] = []
    return render(request, 'my_account.html', context)


# Vendor views moved to myapp2.views

def about(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    return render(request, 'about.html', context)


def menu(request):
    from myapp2.models import Product
    user = _get_session_user(request)
    context = {}
    
    # Get all products initially
    all_products = Product.objects.all()
    
    # Get rating filter from query parameters
    rating_filter = request.GET.get('rating', None)
    
    # Apply rating filter if provided
    # Since products don't have a rating field, we'll simulate ratings based on product ID
    # Products with ID % 5 == 0 get 5 stars, % 5 == 1 get 4 stars, etc.
    if rating_filter:
        try:
            rating = int(rating_filter)
            # Simple rating simulation: filter products and assign simulated ratings
            filtered_products = []
            for product in all_products:
                product_rating = (product.id % 5) if (product.id % 5) != 0 else 5
                if product_rating >= rating:
                    filtered_products.append(product)
            all_products = filtered_products
        except (ValueError, TypeError):
            pass
    
    context['all_products'] = all_products
    context['selected_rating'] = rating_filter
    
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    return render(request, 'menu.html', context)


def blog(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    return render(request, 'blog.html', context)


def blog_details(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    return render(request, 'blog_details.html', context)


def checkout(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
    return render(request, 'checkout.html', context)


@login_required
def cart(request):
    from myapp2.models import Product
    user = _get_session_user(request)
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        aid = Add_to_cart.objects.filter(uid=uid)
        # Pass all products for new branded section
        all_products = Product.objects.all()
        con = {
            'uid': uid,
            'aid': aid,
            'all_products': all_products,
            'cart_count': aid.count()
        }
        if user and user.role == 'customer':
            con['user_name'] = user.name
            con['user_email'] = user.email
        return render(request, 'cart.html', con)
    else:
        # Pass all products even if not logged in
        from myapp2.models import Product
        all_products = Product.objects.all()
        return render(request, 'cart.html', {'all_products': all_products, 'cart_count': 0})


# Add to cart view


@login_required
def add_to_cart(request, id):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        pid = Product.objects.get(id=id)

        # Check if product already exists in user's cart
        existing_item = Add_to_cart.objects.filter(uid=uid, pid=pid).first()

        if existing_item:
            # If product already in cart, increase quantity instead of creating duplicate
            existing_item.qty += 1
            existing_item.total_price = existing_item.price * existing_item.qty
            existing_item.save()
            messages.success(request, f'{pid.name} quantity updated in cart.')
        else:
            # Create new cart item
            Add_to_cart.objects.create(
                uid=uid,
                pid=pid,
                name=pid.name,
                price=pid.price,
                qty=1,
                img=pid.image,
                total_price=pid.price
            )
            messages.success(request, f'{pid.name} added to cart.')

        return redirect('cart')
    else:
        return render(request, 'category_market.html')


def buy_now(request, id):
    """Add product to cart and redirect to billing page for immediate checkout"""
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        pid = Product.objects.get(id=id)

        # Check if product already exists in user's cart
        existing_item = Add_to_cart.objects.filter(uid=uid, pid=pid).first()

        if existing_item:
            # If product already in cart, increase quantity
            existing_item.qty += 1
            existing_item.total_price = existing_item.price * existing_item.qty
            existing_item.save()
        else:
            # Create new cart item
            Add_to_cart.objects.create(
                uid=uid,
                pid=pid,
                name=pid.name,
                price=pid.price,
                qty=1,
                img=pid.image,
                total_price=pid.price
            )
        
        messages.success(request, f'{pid.name} added to cart. Proceeding to checkout.')
        return redirect('billing')
    else:
        return render(request, 'login.html')


@login_required
def remove_cart(request, id):
    rid = Add_to_cart.objects.get(id=id).delete()
    return redirect('cart')


@login_required
def remove_all_cart(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        Add_to_cart.objects.filter(uid=uid).delete()
        messages.success(request, 'All items removed from cart.')
    return redirect('cart')


@login_required
def plus(request, id):
    pid = Add_to_cart.objects.get(id=id)
    if pid:
        pid.qty = pid.qty + 1
        pid.total_price = pid.qty * pid.price
        pid.save()
    return redirect('cart')


@login_required
def minus(request, id):
    mid = Add_to_cart.objects.get(id=id)
    if mid.qty == 1:
        mid.delete()
        return redirect('cart')
    else:
        if mid:
            mid.qty = mid.qty - 1
            mid.total_price = mid.qty * mid.price
            mid.save()
    return redirect('cart')


@login_required
def wishlist(request):
    user = _get_session_user(request)
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        wid = Wishlist.objects.filter(uid=uid)
        con = {
            'uid': uid,
            'wid': wid,
            'cart_count': Add_to_cart.objects.filter(uid=uid).count()
        }
        if user and user.role == 'customer':
            con['user_name'] = user.name
            con['user_email'] = user.email
        return render(request, 'wishlist.html', con)
    else:
        return render(request, 'wishlist.html', {'cart_count': 0})


@login_required
def add_to_wishlist(request, id):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        pid = Product.objects.get(id=id)
        Wishlist.objects.create(
            uid=uid,
            pid=pid,
            name=pid.name,
            desc=getattr(pid, 'description', ''),
            img=pid.image,
            price=pid.price
        )
        return redirect('wishlist')
    else:
        return render(request, 'product_details.html')


@login_required
def remove_wishlist(request, id):
    Wishlist.objects.filter(id=id).delete()
    return redirect('wishlist')


@login_required
def billing(request):
    user = _get_session_user(request)
    uid = User.objects.get(email=request.session['email'])
    cart_items = Add_to_cart.objects.filter(uid=uid)
    
    context = {}
    
    # Add user details
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
    
    # Add cart details
    context['cart_items'] = cart_items
    sub_total = 0
    for item in cart_items:
        sub_total += item.price * item.qty
    
    context['sub_total'] = sub_total
    context['shipping'] = 50
    context['total'] = sub_total + 50
    context['cart_count'] = cart_items.count()
    
    # Fetch and pre-fill with latest address data
    try:
        latest_address = Address.objects.filter(uid=uid).latest('id')
        context['billing_data'] = {
            'first_name': latest_address.first_name,
            'last_name': latest_address.last_name,
            'email': latest_address.email,
            'phone': '',  # Phone not stored in Address model
            'address': latest_address.address,
            'country': latest_address.country,
            'state': latest_address.state,
            'zip_code': latest_address.zip_code,
        }
    except Address.DoesNotExist:
        # If no previous address, use user's email only
        context['billing_data'] = {
            'first_name': '',
            'last_name': '',
            'email': context.get('user_email', ''),
            'phone': '',
            'address': '',
            'country': '',
            'state': '',
            'zip_code': '',
        }
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        state = request.POST['state']

        Address.objects.create(
            uid=uid,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            country=country,
            zip_code=zip_code,
            state=state
        )
        return redirect('checkout')
    else:
        return render(request, "billing.html", context)


@login_required
def checkout(request):
    user = _get_session_user(request)
    uid = User.objects.get(email=request.session['email'])
    prod = Add_to_cart.objects.filter(uid=uid)

    if not prod.exists():
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')

    sub_total = 0
    total = 0

    try:
        for i in prod:
            sub_total += i.price * i.qty

        total = sub_total + 50
        amount = total * 100

        client = razorpay.Client(
            auth=('rzp_test_bilBagOBVTi4lE', '77yKq3N9Wul97JVQcjtIVB5z')
        )

        response = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        })

        context = {
            'uid': uid,
            'prod': prod,
            'response': response,
            'total': total,
            'sub_total': sub_total
        }
        
        if user and user.role == 'customer':
            context['user_name'] = user.name
            context['user_email'] = user.email

        return render(request, "checkout.html", context)

    except Exception as e:
        print(e)
        return render(request, "checkout.html")


@login_required
def success(request):
    uid = User.objects.get(email=request.session['email'])
    cart_items = Add_to_cart.objects.filter(uid=uid)

    if not cart_items.exists():
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')

    sub_total = 0
    items_payload = []
    for item in cart_items:
        sub_total += item.price * item.qty
        items_payload.append({
            'name': item.name,
            'price': item.price,
            'qty': item.qty,
            'total_price': item.price * item.qty
        })

    shipping = 50 if sub_total > 0 else 0
    total = sub_total + shipping

    order = Order.objects.create(
        uid=uid,
        sub_total=sub_total,
        shipping=shipping,
        total_amount=total,
        payment_id=request.GET.get('payment_id', ''),
        payment_order_id=request.GET.get('order_id', ''),
        status='paid',
        items_json=items_payload
    )

    cart_items.delete()
    request.session['last_order_id'] = order.id

    return render(request, "success.html", {'order': order})


@login_required
def invoice_pdf(request, order_id):
    uid = User.objects.get(email=request.session['email'])
    order = Order.objects.filter(id=order_id, uid=uid).first()

    if not order:
        messages.error(request, 'Invoice not found.')
        return redirect('cart')

    items = order.items_json or []
    address = Address.objects.filter(uid=uid).order_by('-id').first()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    # Header Background Box
    from reportlab.lib import colors as rl_colors
    from reportlab.pdfgen import canvas as pdf_canvas
    pdf.setFillColor(rl_colors.HexColor('#2C3E50'))
    pdf.rect(0, y - 60, width, 60, fill=1, stroke=0)
    
    # Company Name - Styled
    pdf.setFont('Helvetica-Bold', 28)
    pdf.setFillColor(rl_colors.HexColor('#FFFFFF'))
    pdf.drawString(40, y - 40, '🏪 TechNova')
    
    pdf.setFont('Helvetica', 9)
    pdf.setFillColor(rl_colors.HexColor('#ECF0F1'))
    pdf.drawString(40, y - 52, 'Your Premium Online Store')
    
    # Invoice text on right
    pdf.setFont('Helvetica-Bold', 16)
    pdf.setFillColor(rl_colors.HexColor('#FFFFFF'))
    pdf.drawRightString(width - 40, y - 40, 'INVOICE')
    
    y -= 80
    
    # Invoice Details - Left Column
    pdf.setFillColor(rl_colors.HexColor('#000000'))
    pdf.setFont('Helvetica-Bold', 11)
    pdf.drawString(40, y, 'INVOICE DETAILS')
    
    pdf.setFont('Helvetica', 9)
    y -= 15
    pdf.drawString(40, y, f"Invoice No.: #{order.id}")
    y -= 12
    pdf.drawString(40, y, f"Date: {timezone.localtime(order.created_at).strftime('%d %b, %Y')}")
    y -= 12
    pdf.drawString(40, y, f"Payment ID: {order.payment_id or 'N/A'}")
    y -= 12
    pdf.drawString(40, y, f"Status: ✓ PAID")
    
    # Customer Details - Right Column
    pdf.setFont('Helvetica-Bold', 11)
    pdf.drawString(300, height - 180, 'BILL TO')
    
    pdf.setFont('Helvetica', 9)
    y_right = height - 195
    pdf.drawString(300, y_right, f"Name: {uid.name}")
    y_right -= 12
    pdf.drawString(300, y_right, f"Email: {uid.email}")
    y_right -= 12
    if address and hasattr(address, 'phone_no'):
        pdf.drawString(300, y_right, f"Phone: {address.phone_no}")
    y_right -= 12
    if address:
        pdf.drawString(300, y_right, f"Address:")
        pdf.drawString(300, y_right - 12, f"{address.address}, {address.state}")
        pdf.drawString(300, y_right - 24, f"{address.country} - {address.zip_code}")
    
    # Divider Line
    y = height - 270
    pdf.setStrokeColor(rl_colors.HexColor('#BDC3C7'))
    pdf.setLineWidth(2)
    pdf.line(40, y, width - 40, y)
    
    # Products Table
    y -= 20
    data = [['Product', 'Qty', 'Unit Price', 'Total']]
    for item in items:
        data.append([item.get('name', ''), str(item.get('qty', 0)),
                    f"₹ {item.get('price', 0)}", f"₹ {item.get('total_price', 0)}"])

    table = Table(data, colWidths=[220, 60, 90, 90])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), rl_colors.HexColor('#ECF0F1')),
        ('GRID', (0, 0), (-1, -1), 1, rl_colors.HexColor('#BDC3C7')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [rl_colors.HexColor('#FFFFFF'), rl_colors.HexColor('#ECF0F1')]),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    table_width, table_height = table.wrap(0, 0)
    table.drawOn(pdf, 40, y - table_height)
    y = y - table_height - 30

    # Divider Line
    pdf.setStrokeColor(rl_colors.HexColor('#BDC3C7'))
    pdf.setLineWidth(1)
    pdf.line(40, y, width - 40, y)
    
    y -= 20
    
    # Summary Box
    summary_y = y
    pdf.setFillColor(rl_colors.HexColor('#ECF0F1'))
    pdf.rect(280, summary_y - 90, 240, 90, fill=1, stroke=1)
    pdf.setStrokeColor(rl_colors.HexColor('#34495E'))
    pdf.setLineWidth(2)
    
    # Amount Details
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(rl_colors.HexColor('#000000'))
    pdf.drawString(300, summary_y - 20, 'Subtotal:')
    pdf.drawRightString(500, summary_y - 20, f"₹ {order.sub_total}")
    
    pdf.drawString(300, summary_y - 40, 'Shipping:')
    pdf.drawRightString(500, summary_y - 40, f"₹ {order.shipping}")
    
    # Total Line
    pdf.setLineWidth(1)
    pdf.line(300, summary_y - 50, 500, summary_y - 50)
    
    pdf.setFont('Helvetica-Bold', 13)
    pdf.setFillColor(rl_colors.HexColor('#E74C3C'))
    pdf.drawString(300, summary_y - 70, 'Total Amount:')
    pdf.drawRightString(500, summary_y - 70, f"₹ {order.total_amount}")
    
    # Footer
    footer_y = 30
    pdf.setFont('Helvetica', 8)
    pdf.setFillColor(rl_colors.HexColor('#7F8C8D'))
    pdf.drawString(40, footer_y, 'Thank you for your purchase! | TechNova - Your Premium Online Store')
    pdf.drawString(40, footer_y - 10, f'Invoice ID: TechNova-{order.id} | Generated on {timezone.now().strftime("%d-%m-%Y %H:%M")}')

    pdf.drawString(40, footer_y - 10, f'Invoice ID: TechNova-{order.id} | Generated on {timezone.now().strftime("%d-%m-%Y %H:%M")}')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="TechNova-Invoice-{order.id}.pdf"'
    return response


def order_successfull(request):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
    return render(request, 'checkout.html', context)


def product_details(request, product_id):
    user = _get_session_user(request)
    if user and user.role == 'vendor':
        return redirect('vendor:vendor_dashboard')
    context = {}
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    # Pass all other products as related_products (excluding the current one)
    related_products = Product.objects.exclude(id=product_id)
    context['related_products'] = related_products
    if user and user.role == 'customer':
        context['user_name'] = user.name
        context['user_email'] = user.email
        context['cart_count'] = Add_to_cart.objects.filter(uid=user).count()
    else:
        context['cart_count'] = 0
    return render(request, 'product_details.html', context)


def subscribe_newsletter(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter an email address.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        try:
            # Check if email already exists
            subscription, created = NewsletterSubscription.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'This email is already subscribed to our newsletter.')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
            print(f"Newsletter subscription error: {e}")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')
