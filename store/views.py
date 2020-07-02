# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth import authenticate, logout as logout_method, login as login_method 
from django.contrib.auth.models import User
from django.template.response import TemplateResponse


# Local
from . models import Product, Address, UserAddress, PasswordResetRequest, Order, OrderItem, Delivery, UnitType


######################################## INDEX ########################################
def index(request):
    # Assume the user is not an employee
    user_is_employee = False

    # Request user
    user = request.user

    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    # Get the 5 latest products to display
    products = Product.objects.all()[:3]

    # TEST
    context = {
        'user_is_employee': user_is_employee, 
        'products': products
    }

    # Response
    return TemplateResponse(request, 'store/index.html', context=context)


######################################## PRODUCTS ########################################
def product_list(request):
    # Request user
    user = request.user

    # Assume the user is not an employee    
    user_is_employee = False

    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    # Query all active products
    queryset = Product.objects.filter(active=True)

    # Store context dict
    context = {
        'products': queryset,
        'user_is_employee': user_is_employee
    }

    # Response
    return TemplateResponse(request, 'store/product-list.html', context=context)

def product_detail(request, pk):
    # Get product
    product = get_object_or_404(Product, pk=pk)

    # Assume that user is not employee
    user_is_employee = False

    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    # Save context dict
    context = {
        'product': product,
        'user_is_employee': user_is_employee
    }

    # Response
    return TemplateResponse(request, 'store/product-detail.html', context=context)

def product_create(request):
    # Check for perms
    if request.user.is_authenticated:
        if request.method == "POST":
            # Create new Product
            product                 = Product()
            product.title           = request.POST['txtTitle']
            product.subtitle        = request.POST['txtSubtitle']
            product.description     = request.POST['txtDescription']
            product.unit_type       = get_object_or_404(UnitType, pk=request.POST['txtUnitType'])
            product.unit_price      = request.POST['numUnitPrice']
            product.unit            = request.POST['numUnit']
            product.image           = request.POST['txtImageUrl']
            # Save !!!
            product.save()
            # Send the user back to products
            return HttpResponseRedirect(reverse('product-list'))
    
    unit_types = UnitType.objects.all()
    context = {
        'unit_types': unit_types
    }
    return TemplateResponse(request, 'store/product-create.html', context=context)

def product_delete(request, pk):
    if Product.objects.filter(pk=pk).exists():
        product_to_delete = get_object_or_404(Product, pk=pk)
        product_to_delete.active = False
        product_to_delete.save()
    return redirect('product-list')


######################################## USER REGISTRATION ########################################
def signup(request):
    # Check if user is already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))

    context = {}

    # Handle POST request data
    if request.method == "POST":
        username            = request.POST['txtUsername']
        firstname           = request.POST['txtFirstname']
        lastname            = request.POST['txtLastname']
        email               = request.POST['txtEmail']
        password            = request.POST['txtPassword']
        confirm_password    = request.POST['txtConfirmPassword']

        # Check if password is correctly typed
        if password == confirm_password:
            # Create new user
            user            = User()
            user.username   = username
            user.first_name = firstname
            user.last_name  = lastname
            user.email      = email
            user.password   = password
            
            # Save!!!
            user.save()

            # Response message
            if user:
                login_method(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                context = {
                    'error': 'Could not create user account - please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }

    # Resposne
    return TemplateResponse(request, 'store/signup.html', context)


######################################## PROFILE ########################################
def profile(request):
    # Redirect if user is already logged in
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    user_is_employee = False
    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    # Query user's address book and orders
    user_address_book   = UserAddress.objects.filter(user=request.user, active=True)
    user_orders         = Order.objects.filter(customer=request.user)

    # Save context dict
    context = {
        'user': request.user,
        'user_address_book': user_address_book,
        'user_orders': user_orders,
        'user_is_employee': user_is_employee
    }

    # Response
    return TemplateResponse(request, 'store/profile.html', context=context)

def add_address(request):
    user = request.user
    context = {}
    if request.method == "POST":
        newAddress              = Address()
        postal                  = request.POST['txtPostal']
        city                    = request.POST['txtCity']
        street                  = request.POST['txtStreet']
        number                  = request.POST['txtNumber']
        floor                   = request.POST['txtFloor']
        direction               = request.POST['txtDirection']
        newAddress.postal       = postal
        newAddress.city         = city
        newAddress.street       = street
        newAddress.number       = number
        newAddress.floor        = floor
        newAddress.direction    = direction
        newAddress.save()
        useraddress             = UserAddress()
        useraddress.user        = request.user
        useraddress.address     = newAddress
        useraddress.save()
    return HttpResponseRedirect(reverse('profile'))

def delete_address(request, pk):
    user_address_to_delete          = get_object_or_404(UserAddress, pk=pk)
    user_address_to_delete.active   = False
    user_address_to_delete.save()
    return HttpResponseRedirect(reverse('profile'))


######################################## LOG IN/OUT ########################################
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))

    context = {}
    if request.method == "POST":
        user = authenticate(username=request.POST['txtUsername'], password=request.POST['txtPassword'])
        if user:
            login_method(request, user)
            return HttpResponseRedirect(reverse('profile'))
        else:
            context = {
                'error': 'Bad username or password.'
            }
    return TemplateResponse(request, 'store/login.html', context)

def logout(request):
    logout_method(request)
    return TemplateResponse(request, 'store/login.html')


######################################## PASSWORD RESET ########################################
def password_reset(request):
    if request.method == "POST":
        user = request.POST['txtUserId']
        newPassword = request.POST['txtNewPassword']
        newPasswordConfirm = request.POST['txtNewPasswordConfirm']
        token = request.POST['txtToken']

        if newPassword == newPasswordConfirm:
            try:
                prr = PasswordResetRequest.objects.get(token=token)
                prr.save()

            except:
                print(f'Invalid password reset attempt')
                return TemplateResponse(request, 'store/password-reset.html')

            user = prr.user
            user.set_password(password)
            user.save()

            return HttpResponseRedirect(reverse('login'))
    return TemplateResponse(request, 'store/password_reset.html')

def password_reset_request(request):
    if request.method == "POST":
        username = request.POST['txtUsername']
        user = None

        if username:
            try:
                user = User.objects.get(username=username)
            except:
                print(f'invalid password reset request: {user}')
        else:
            user = request.POST['txtUserEmail']
            try:
                user = User.objects.get(email=user)
            except:
                print(f'invalid password reset request: {user}')

        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            return HttpResponseRedirect(reverse('password-reset'))
    return TemplateResponse(request, 'store/password-reset-request.html')


######################################## ORDERS #########################################
def get_incomplete_order(request):
    user = get_object_or_404(User, pk=request.user.pk)
    order = Order.objects.filter(customer=user, status="P")
    if order.exists():
        return order[0]
    return 0

def product_add_to_cart(request, pk):
    user = get_object_or_404(User, pk=request.user.pk)
    product_to_add = get_object_or_404(Product, pk=pk)
    order_to_append_to = None
    # Create new ordre if no incomplete exists,
    if get_incomplete_order(request) == 0:
        order_to_append_to = Order()
        order_to_append_to.customer = user
        order_to_append_to.save()
    else:
        order_to_append_to = get_incomplete_order(request)

    # Check if the product is already added
    if OrderItem.objects.filter(order=order_to_append_to, product=product_to_add).exists():
        orderitem = get_object_or_404(
            OrderItem, order=order_to_append_to, product=product_to_add)
        orderitem.quantity += int(1)
        orderitem.save()
    else:
        orderitem = OrderItem()
        orderitem.order = order_to_append_to
        orderitem.product = product_to_add
        orderitem.save()
    return redirect('cart')

def edit_quantity(request, pk):
    cart_item = get_object_or_404(OrderItem, pk=pk)
    if request.method == "POST":
        if cart_item:
            new_quantity = request.POST['nNewQuantity']
            if new_quantity != cart_item.quantity:
                cart_item.quantity = int(new_quantity)
                cart_item.save()
    return redirect('cart')

def remove_from_cart(request, pk):
    order_item = OrderItem.objects.filter(pk=pk)
    order_item.delete()

    return redirect('cart')

def edit_quantity(request, pk):
    cart_item = get_object_or_404(OrderItem, pk=pk)

    if request.method == "POST":
        if cart_item:
            new_quantity = request.POST['nNewQuantity']
            if new_quantity != cart_item.quantity:
                cart_item.quantity = int(new_quantity)
                cart_item.save()
    return redirect('cart')

def cart(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    user_is_employee = False
    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    context = {
        'error_message': 'You\'re cart is empty',
    }

    pending_order = get_incomplete_order(request)

    if pending_order == 0:
        order_items = 0
    else:
        order_items = OrderItem.objects.filter(order=pending_order)
        order_total = 0
        for order_item in order_items:
            order_total += order_item.get_total_price()
        items_amount = 0
        for order_item in order_items:
            items_amount += order_item.quantity

        context = {
            'message': None,
            'order_items': order_items,
            'order': pending_order,
            'order_total': order_total,
            'items_amount': items_amount,
            'user_is_employee': user_is_employee,
        }

    return TemplateResponse(request, 'store/cart.html', context=context)

def checkout(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    user_addresses = UserAddress.objects.filter(user=request.user)
    
    user_is_employee = False
    # Chech for perms
    if request.user.has_perm('store.change_product'):
        user_is_employee = True

    context = {
        'order': order,
        'order_items': order_items,
        'user_addresses': user_addresses,
        'user_is_employee': user_is_employee

    }
    return TemplateResponse(request, 'store/checkout.html', context=context)

def make_order_ready_for_delivery(request, pk):
    if request.method == "POST":
        delivery = Delivery()
        order = get_object_or_404(Order, pk=pk)
        order.status = "P"
        order.save()
        address = get_object_or_404(
            Address, pk=request.POST['selectDeliveryAddress'])
        delivery.address = address
        delivery.order = order
        delivery.save()
    return HttpResponseRedirect(reverse('profile'))