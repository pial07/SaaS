"""
URL configuration for home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from auth import views as auth_views
from checkouts import views as checkout_views
from subscriptions import views as subscription_views
from landing import views as landing_views

urlpatterns = [
    path('', landing_views.landing_page_view, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='login'),
    path('checkout/sub-price/<int:price_id>/', checkout_views.product_price_redirect_view, name='sub-price-checkout'),
    path('checkout/start/', checkout_views.checkout_redirect_view, name='stripe-checkout-start'),
    path('checkout/success/', checkout_views.checkout_finalize_view, name='stripe-checkout-end'),
    path('pricing/', subscription_views.subscription_price_view, name='pricing'),
    path('pricing/<str:interval>/', subscription_views.subscription_price_view, name='interval-pricing'),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('protected/', views.pwd_protected_view, name='pwd_protected_view'),
    path('protected/user-only', views.user_only_view, name='user-only-view'),
    path('protected/staff-only', views.staff_only_view, name='staff-only-view'),
    path('accounts/billing', subscription_views.user_subscription_view, name='user-subscription'),
    path('accounts/billing/cancel', subscription_views.user_subscription_cancel_view, name='user-subscription-cancel'),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
]
