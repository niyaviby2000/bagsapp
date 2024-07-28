"""
URL configuration for BagsShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from bagsstore import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/',views.RegistrationView.as_view(),name="register"),

    path('',views.LoginInView.as_view(),name="signin"),

    path('index/',views.IndexView.as_view(),name="index"),

    path('bags/<int:pk>/',views.BagDetailView.as_view(),name="bag-detail"),

    path('bags/<int:pk>/cart/add',views.AddToCartView.as_view(),name="cart-add"),

    path('cart/all/',views.CartSummaryView.as_view(),name="cart-summary"),

    path('cart/<int:pk>/remove/',views.CartDestroyView.as_view(),name="cart-remove"),

    path('signout/',views.SignOutView.as_view(),name="signout"),

    path('Basketitem/quantity/<int:pk>/change/',views.CartQuantityUpdateView.as_view(),name="cartqty-update"),

    path('placeorder/',views.PlaceOrderView.as_view(),name="place-order"),

    path('order/summary/',views.OrderSummaryView.as_view(),name="order-summary"),

    path('api/',include("api.urls")),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
