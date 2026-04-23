"""
URL configuration for GLHSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GLHApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.aboutUs, name='aboutUs'),
    path('producer/', views.producer, name='producer'),
    path('product/', views.product, name='product'),
    path('admin/', admin.site.urls),
    
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    
    path('product/<int:pk>/', views.individualProductPage, name='individualProductPage'),
    path('producer/<int:pk>/', views.individualProducerPage, name='individualProducerPage'),

    #Producer specific
    path('add-product/', views.addProduct, name='addProduct'),
    path('edit-product/', views.editProduct, name='editProduct'),
    path('producer-dashboard/', views.producerDashboard, name='producerDashboard'),

    #Customer specific
    path('customer-dashboard/', views.customerDashboard, name='customerDashboard'),

    #Cart system
    path('user-cart-view/', views.userCartView, name='userCartView'),
    path('add-product-to-cart/<int:pk>', views.addProductToUserCart, name='addProductToUserCart'),
    path('increase-product-quantity-in-cart/<int:pk>', views.increaseProductQuantityInCart, name='increaseProductQuantityInCart'),
    path('remove-product-from-cart/<int:pk>', views.decreaseProductQuantityOrDeleteProductInCart, name='decreaseProductQuantityOrDeleteProductInCart'),

    #Order system
    path('checkout-and-confirm-order-details/', views.checkoutAndConfirmOrderDetails, name='checkoutAndConfirmOrderDetails'),
    path('customer-places-order/', views.customerPlacesOrder, name='customerPlacesOrder'),
    path('customer-order-confirmation/<int:order_id>/', views.customerOrderConfirmation, name='customerOrderConfirmation'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)