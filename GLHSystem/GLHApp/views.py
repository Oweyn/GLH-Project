from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LoginForm
from ProducerProducts.models import Product, Allergen
from UserAccounts.models import ProducerAccount
from ProducerProducts.forms import AddProductForm, EditProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from UserCarts.models import Cart, CartItem, get_user_cart
from UserOrders.models import Order, OrderItem
import math
from decimal import Decimal
#TODO: Consider shortinging imports?

# Create your views here.

def index(request):
    return render(request, 'index.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def individualProductPage(request, pk):
    products = Product.objects.get(pk=pk)
    return render(request, 'individualProductPage.html', {'product': products})

def producer(request):
    producers = ProducerAccount.objects.all()
    return render(request, 'producer.html', {'producers': producers})

def individualProducerPage(request, pk):
    producer = ProducerAccount.objects.get(pk=pk)
    products = Product.objects.filter(producer=producer)
    return render(request, 'individualProducerPage.html', {'producer': producer, 'products': products})

#Includes the allergen filter
def product(request):
    products = Product.objects.all()
    allergens = Allergen.objects.all()
    allergens = Allergen.objects.exclude(allergen_name="No applicable allergens")
    selected_allergens = request.GET.getlist('product_allergens')
    
    if selected_allergens:
        products = products.exclude(product_allergens__id__in=selected_allergens)

    return render(request, 'product.html', {
        'products': products,
        'allergens': allergens,
        'selected_allergens': selected_allergens
    })

#Producer view only
@login_required
def addProduct(request):
    if not request.user.is_producer:
        return render(request, 'index.html')#TODO: to change this to a redirect with an error message

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.producer = request.user.produceraccount
            new_product.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = AddProductForm()

    return render(request, 'addProduct.html', {'form': form})

#Allows producers to edit there exsisting products
#TODO: Logic check
@login_required
def editProduct(request, pk):
    permission = request.user.produceraccount
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            new_product_detail = form.save(commit=False)
            new_product_detail.producer = request.user.produceraccount
            new_product_detail.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = EditProductForm(instance=product)

    return render(request, 'editProduct.html', {'form': form})

#Login system
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {"form": form})

def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Incorrect username or password.')#TODO: Change to a python alert box or similair
    else:
        form=LoginForm()
    return render(request, 'login.html', {'form': form})

def logoutPage(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')
    return render(request, 'logout.html')

#TODO: Logic check
#Customer and producer dashboards
@login_required
def producerDashboard(request):
    if not request.user.is_producer:
        return render(request, 'index.html')#TODO: to change this to a redirect
    
    producer = request.user.producer
    producer_products = Product.objects.filter(producer=producer)
    individual_order_items = OrderItem.objects.filter(product__producer=producer).select_related('order', 'order__user')

        #if new_status in valid_statuses:
     #   order = get_object_or_404(Order, id=order_id, items__product__producer=producer)
      #  order.status = new_status
       # order.save()
        #Add success image

        #return redirect('producer_dashboard')

    return render(request, 'producerDashboard.html', {
        'producer' : producer,
        'producer_products' : producer_products,
        'individual_order_items' : individual_order_items,
        })

@login_required
def customerDashboard(request):
    active_and_past_customer_orders = Order.objects.filter(customer=request.user)
    return render(request, 'customerDashboard.html',{
        'orders': active_and_past_customer_orders,
        'user': request.user,
    })

#Cart system
@login_required
def userCartView(request):
    user_cart = get_user_cart(request.user)
    avilavle_items = user_cart.cart_items.all()
    cart_items = []
    cart_subtotal = 0
    #TODO: Consider if this could be made into a resuable function?
    for item in avilavle_items:
        line_total = item.subtotal()
        cart_subtotal += line_total

        cart_items.append({
            "product": item.product,
            "quantity": item.quantity,
            "line_total": line_total,
        })
    return render(request, 'userCartView.html', {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal
    })


#TODO: Consider annoymous users, they will not be able to access the system
#TODO: Consider a fucntion to avoid code redundancy or combining all these cart management functions
@login_required
def addProductToUserCart(request, pk):
    #TODO: Add exception handling in case a product is not found
    product = Product.objects.get(pk=pk)
    cart = get_user_cart(request.user)

    if product.stock < 1:
    #TODO: Item out of stock error message as well as a redirect
        return redirect('userCartView')
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if cart_item.quantity >= product.stock:
        return redirect('userCartView')

    cart_item.quantity += 1
    cart_item.save()
    return redirect('individualProductPage', pk=product.pk)

@login_required
def increaseProductQuantityInCart(request, pk):
    product = Product.objects.get(pk=pk)
    cart = get_user_cart(request.user)

    if product.stock < 1:
    #TODO: Item out of stock error message as well as a redirect
        return redirect('userCartView')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if cart_item.quantity >= product.stock:
        #TODO: add an error message
        return redirect('userCartView')

    cart_item.quantity += 1
    cart_item.save()
    return redirect('userCartView')

@login_required
def decreaseProductQuantityOrDeleteProductInCart(request, pk):
    product = Product.objects.get(pk=pk)
    cart = get_user_cart(request.user)

    if product.stock < 1:
        return render(request, 'userCartView.html')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
    cart_item.save()
    return redirect('userCartView')

#Order system
#TODO: Logic check
@login_required
def checkoutAndConfirmOrderDetails(request):
    user_cart = get_user_cart(request.user)
    if not user_cart:
        #TODO: add error message
        return redirect('userCartView')
    avilable_items = user_cart.cart_items.all()
        
    final_items = []
    cart_subtotal = 0
    delivery_order = request.POST.get('delivery_order')
    if delivery_order == True:
        delivery_address = request.POST.get('customer_delivery_address')
        #TODO: Add validation
    
    for item in avilable_items:
        if item.quantity > item.product.stock:
            #TODO: Need to add a now out of stock error message / or a disabled button
            return render(request, 'userCartView.html')

        cart_product = item.product
        item_total = cart_product.price * item.quantity
        cart_subtotal += item_total
        final_items.append({'cart_product': cart_product,
                        'quantity': item.quantity,
                        'item_total': item_total,})
    
    return render(request, 'customerCheckout.html', {
        'items': final_items,
        'cart_subtotal': cart_subtotal
})

#This is where loyalty points are calculated    
@login_required
def customerPlacesOrder(request):
    user_cart = get_user_cart(request.user)
    if not user_cart:
        #TODO: Add error message
        return redirect('userCartView')
    
    avilable_items = user_cart.cart_items.all()
    customer_delivery_address = request.POST.get('customer_delivery_address')
    cart_total = 0
    cart_subtotal = 0
    delivery_charge = Decimal(3.75)
    #The prototype is using a dummy payment system, there is a fixed delivery charge. However this would be changed to be caluclated depedning on how far the customer lives

    for item in avilable_items:
        if item.quantity > item.product.stock:
            #TODO: Need to add a now out of stock error message
            return render(request, 'userCartView.html')

        cart_product = item.product
        item_total = cart_product.price * item.quantity
        cart_subtotal += item_total
    
    delivery_order = request.POST.get('delivery_order')
    loyalty_points_earned = math.floor(cart_subtotal * 10)

    if delivery_order == True:
        cart_total = cart_subtotal + delivery_charge

        customer_order = Order.objects.create(
        customer = request.user,
        is_completed = False,
        delivery_order = True,
        total_order_price = cart_total,
        customer_delivery_address = customer_delivery_address,
        loyalty_points_earned = loyalty_points_earned
    )
    else:
#TODO: Double check django is automatically adding the correct info for created_at data
        cart_total = cart_subtotal
        customer_order = Order.objects.create(
        customer = request.user,
        is_completed = False,
        delivery_order = False,
        total_order_price = cart_total,
        customer_delivery_address = customer_delivery_address,
        loyalty_points_earned = loyalty_points_earned
    )

    for item in avilable_items:
        cart_product = item.product
        OrderItem.objects.create(
            order = customer_order,
            product = item.product,
            quantity = item.quantity,
            individal_item_price = cart_product.price,
        )

        cart_product.stock -= item.quantity
        cart_product.save()

    request.user.user_loyalty_points += loyalty_points_earned
    request.user.save()
    user_cart.delete()

    #TODO:Add a Sucess message
    return redirect('customerOrderConfirmation', customer_order.id)

@login_required
def customerOrderConfirmation(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)
    return render(request, 'customerOrderConfirmation.html', {'order': order})