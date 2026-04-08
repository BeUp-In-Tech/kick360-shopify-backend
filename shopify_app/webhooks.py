# import json
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import EmailMultiAlternatives

# from .models import AccessCode
# from .utils import generate_access_code


# @csrf_exempt
# def order_paid_webhook(request):

#     data = json.loads(request.body)

#     email = data.get("email") or data.get("customer", {}).get("email")
#     order_id = str(data.get("id"))

#     if not email or not order_id:
#         return HttpResponse("Invalid data")

#     if AccessCode.objects.filter(order_id=order_id).exists():
#         print("Duplicate webhook ignored:", order_id)
#         return HttpResponse("Already processed")

#     code = generate_access_code()

#     AccessCode.objects.create(
#         order_id=order_id,
#         email=email,
#         code=code
#     )

#     text_content = f"""
# Hello,

# Your purchase was successful.

# Your Kick360 access code:
# {code}

# Use this code to create your account and log in.

# Best regards,
# Kick360 Team
# """

#     html_content = f"""
# <html>
#   <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    
#     <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; text-align: center;">
      
#       <h2 style="color: #333;">Kick360 Access Code</h2>

#       <p>Hello,</p>

#       <p>Your purchase was successful.</p>

#       <p>Please use the following access code to create your account and log in:</p>

#       <div style="
#         margin: 20px 0;
#         padding: 15px;
#         background: #fff3f3;
#         border-radius: 10px;
#         display: inline-block;
#       ">
#         <span style="
#           color: #ff3b3b;
#           font-size: 32px;
#           font-weight: bold;
#           letter-spacing: 3px;
#         ">
#           {code}
#         </span>
#       </div>

#       <p>This code is required to access your Kick360 app account.</p>

#       <p style="margin-top: 30px;">Best regards,<br><b>Kick360 Team</b></p>

#     </div>

#   </body>
# </html>
# """

#     email_message = EmailMultiAlternatives(
#         subject="Your Kick360 Access Code",
#         body=text_content,
#         from_email="hamim.leon@gmail.com",
#         to=[email],
#     )

#     email_message.attach_alternative(html_content, "text/html")
#     email_message.send()

#     print("Saved:", email, code)

#     return HttpResponse("Webhook received")


### Updated version using Postmark for email sending

# import json
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from postmarker.core import PostmarkClient
# from django.conf import settings

# from .models import AccessCode
# from .utils import generate_access_code


# @csrf_exempt
# def order_paid_webhook(request):

#     data = json.loads(request.body)

#     email = data.get("email") or data.get("customer", {}).get("email")
#     order_id = str(data.get("id"))

#     if not email or not order_id:
#         return HttpResponse("Invalid data")

#     if AccessCode.objects.filter(order_id=order_id).exists():
#         print("Duplicate webhook ignored:", order_id)
#         return HttpResponse("Already processed")

#     code = generate_access_code()

#     AccessCode.objects.create(
#         order_id=order_id,
#         email=email,
#         code=code
#     )

#     text_content = f"""
# Hello,

# Your purchase was successful.

# Your Kick360 access code:
# {code}

# Use this code to create your account and log in.

# Best regards,
# Kick360 Team
# """

#     html_content = f"""
# <html>
#   <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    
#     <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; text-align: center;">
      
#       <h2 style="color: #333;">Kick360 Access Code</h2>

#       <p>Hello,</p>

#       <p>Your purchase was successful.</p>

#       <p>Please use the following access code to create your account and log in:</p>

#       <div style="margin: 20px 0; padding: 15px; background: #fff3f3; border-radius: 10px; display: inline-block;">
#         <span style="color: #ff3b3b; font-size: 32px; font-weight: bold; letter-spacing: 3px;">
#           {code}
#         </span>
#       </div>

#       <p>This code is required to access your Kick360 app account.</p>

#       <p style="margin-top: 30px;">Best regards,<br><b>Kick360 Team</b></p>

#     </div>

#   </body>
# </html>
# """

#     try:
#         pm = PostmarkClient(server_token=settings.POSTMARK_API_TOKEN)

#         pm.emails.send(
#             From=settings.DEFAULT_FROM_EMAIL,
#             To=email,
#             Subject="Your Kick360 Access Code",
#             HtmlBody=html_content,
#             TextBody=text_content,
#             MessageStream="outbound"
#         )

#         print("Email sent successfully to:", email)

#     except Exception as e:
#         print("Email failed:", str(e))
#         print(f"Code still saved for {email}: {code}")

#     print("Saved:", email, code)

#     return HttpResponse("Webhook received")

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from postmarker.core import PostmarkClient
from django.conf import settings

from .models import AccessCode
from .utils import generate_access_code


# ✅ PRODUCTS THAT SHOULD TRIGGER EMAIL
ALLOWED_PRODUCT_IDS = [
    15676214116687,
    15205780422991
]


@csrf_exempt
def order_paid_webhook(request):

    data = json.loads(request.body)

    email = data.get("email") or data.get("customer", {}).get("email")
    order_id = str(data.get("id"))

    if not email or not order_id:
        return HttpResponse("Invalid data")

    if AccessCode.objects.filter(order_id=order_id).exists():
        print("Duplicate webhook ignored:", order_id)
        return HttpResponse("Already processed")

    # ✅ GET PRODUCT IDS FROM LINE ITEMS
    line_items = data.get("line_items", [])
    purchased_product_ids = [item.get("product_id") for item in line_items]

    print("Purchased products:", purchased_product_ids)

    # ✅ CHECK IF ANY MATCH
    should_send_email = any(
        pid in ALLOWED_PRODUCT_IDS for pid in purchased_product_ids
    )

    code = generate_access_code()

    access = AccessCode.objects.create(
        order_id=order_id,
        email=email,
        code=code,
        email_sent=False  # default
    )

    # ----------------------------------------
    # EMAIL CONTENT
    # ----------------------------------------

    text_content = f"""
Hello,

Your purchase was successful.

Your Kick360 access code:
{code}

Use this code to create your account and log in.

Best regards,
Kick360 Team
"""

    html_content = f"""
<html>
  <body style="font-family: Arial; background:#f9f9f9; padding:20px;">
    <div style="max-width:500px;margin:auto;background:white;padding:20px;border-radius:10px;text-align:center;">
      <h2>Kick360 Access Code</h2>
      <p>Your code:</p>
      <h1 style="color:red;">{code}</h1>
    </div>
  </body>
</html>
"""

    # ----------------------------------------
    # SEND EMAIL ONLY IF PRODUCT MATCHES
    # ----------------------------------------

    if should_send_email:
        try:
            pm = PostmarkClient(server_token=settings.POSTMARK_API_TOKEN)

            pm.emails.send(
                From=settings.DEFAULT_FROM_EMAIL,
                To=email,
                Subject="Your Kick360 Access Code",
                HtmlBody=html_content,
                TextBody=text_content,
                MessageStream="outbound"
            )

            access.email_sent = True
            access.save()

            print("✅ Email sent to:", email)

        except Exception as e:
            print("❌ Email failed:", str(e))

    else:
        print("🚫 Email NOT sent (product not matched)")

    print("Saved:", email, code)

    return HttpResponse("Webhook received")