from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from datetime import date
from flask import request
import os
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

load_dotenv()  # Load .env values if running locally

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")  # Always keep secret key safe

# Setup Flask-Mail with corrected configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'businessconnectrsa@gmail.com'
app.config['MAIL_PASSWORD'] = 'upytpexovucqaiqx'  # Using app password
app.config['MAIL_DEFAULT_SENDER'] = 'businessconnectrsa@gmail.com'

mail = Mail(app)

# --------------- DATABASE CONFIG -----------------
# Try to get hosted DB URL (e.g., from Railway / Render)
DATABASE_URL = os.environ.get('DATABASE_URL')


# If no hosted DB found, use local DB
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
<<<<<<< Updated upstream
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin2023@localhost:5432/businessconnect"
=======
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Maxelo%402023@localhost:5432/businessconnect"
>>>>>>> Stashed changes

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Fixed Email Templates with escaped curly braces
WELCOME_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #27ae60; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Business Connect! 🎉</h1>
        </div>
        <div class="content">
            <div class="success">Your Account is Ready!</div>
           
            <div class="details">
                <h3>Account Details:</h3>
                <div class="detail-item"><span class="label">Name:</span> {name}</div>
                <div class="detail-item"><span class="label">Email:</span> {email}</div>
                <div class="detail-item"><span class="label">User Type:</span> {user_type}</div>
                <div class="detail-item"><span class="label">Phone:</span> {phone}</div>
                <div class="detail-item"><span class="label">Registration Date:</span> {reg_date}</div>
            </div>
           
            <p>Thank you for joining Business Connect! We're excited to have you on board.</p>
           
            <div style="text-align: center;">
                <a href="{login_url}" class="button">Login to Your Account</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Growing Together</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BUSINESS_REGISTRATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Business Profile Registered! ✅</h1>
        </div>
        <div class="content">
            <div class="success">Your Business is Live!</div>
           
            <div class="details">
                <h3>Business Details:</h3>
                <div class="detail-item"><span class="label">Business Name:</span> {title}</div>
                <div class="detail-item"><span class="label">Location:</span> {location}</div>
                <div class="detail-item"><span class="label">Business Type:</span> {bus_type}</div>
                <div class="detail-item"><span class="label">Address:</span> {address}</div>
                <div class="detail-item"><span class="label">Years in Business:</span> {num_years}</div>
            </div>
           
            <p>Your business profile has been successfully registered on Business Connect!</p>
            <p>You can now start adding services and accepting bookings from customers.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Go to Business Dashboard</a>
            </div>
           
            <div class="footer">
                 <p><strong>Business Connect</strong> - Growing Together</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_NOTIFICATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .alert {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .special-request {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 15px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Booking Received! 🎉</h1>
        </div>
        <div class="content">
            <div class="alert">
                <h2>You Have a New Booking!</h2>
                <p>A customer has booked your service</p>
            </div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Service Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service Category:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Customer Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Name:</span>
                        <span class="detail-value">{customer_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">{customer_email}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Phone:</span>
                        <span class="detail-value">{customer_phone}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Booking Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Status:</span>
                        <span class="detail-value" style="color: #f39c12; font-weight: bold;">Pending Confirmation</span>
                    </div>
                </div>
            </div>
           
            {special_request_html}
           
            <p><strong>Action Required:</strong> Please contact the customer within 24 hours to confirm this booking.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View Booking in Dashboard</a>
            </div>
           
            <div class="footer">
               
                <p>This is an automated notification. Please do not reply to this email.</p>

                 <p><strong>Business Connect</strong> - Growing Together</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
NEW_BUSINESS_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .announcement {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .business-details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #9b59b6; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .owner-info {{ background: #e8f6f3; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 New Business Joined!</h1>
        </div>
        <div class="content">
            <div class="announcement">
                <h2>Exciting News!</h2>
                <p>A new business has joined Business Connect</p>
            </div>
           
            <div class="business-details">
                <h3>🎯 Business Information</h3>
                <div class="detail-item">
                    <span class="label">Business Name:</span>
                    <span>{business_name}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Business Type:</span>
                    <span>{business_type}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Location:</span>
                    <span>{business_location}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Stated in:</span>
                    <span>{years_experience} </span>
                </div>
                <div class="detail-item">
                    <span class="label">Description:</span>
                    <span>{business_description}</span>
                </div>
            </div>
           
            <div class="owner-info">
                <h3>👤 Business Owner</h3>
                <div class="detail-item">
                    <span class="label">Owner Name:</span>
                    <span>{owner_name}</span>
                </div>
            </div>
           
            <p><strong>What this means for you:</strong></p>
            <ul>
                <li>✅ More service options available</li>
                <li>✅ Increased competition for better prices</li>
                <li>✅ Expanded network of professionals</li>
                <li>✅ More choices for your needs</li>
            </ul>
           
            <p>Check out their services and see what they have to offer!</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">📋 View All Businesses</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Growing Together</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_CONFIRMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .special-request {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 15px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Booking Sent! ✅</h1>
        </div>
        <div class="content">
            <div class="success">Your Booking is Sent!</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Contact Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Business Phone:</span>
                        <span class="detail-value">{business_phone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business Email:</span>
                        <span class="detail-value">{business_email}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                   
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
            </div>
           
            {special_request_html}
           
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>The business owner will contact you within 24 hours</li>
                <li>You can view your booking status in your dashboard</li>
                <li>Prepare any necessary information for the service</li>
            </ul>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View My Bookings</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Growing Together</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_APPROVED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Booking Approved!</h1>
        </div>
        <div class="content">
            <div class="success">Great News! Your booking has been approved</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Contact Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Business Phone:</span>
                        <span class="detail-value">{business_phone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business Email:</span>
                        <span class="detail-value">{business_email}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Next Steps</h3>
                    <p>The business owner will contact you shortly to arrange the service details.</p>
                    <p>Please keep your phone available and check your messages regularly.</p>
                </div>
            </div>
           
            <p><strong>What to expect next:</strong></p>
            <ul>
                <li>📞 The business owner will contact you within 24 hours</li>
                <li>📅 Schedule the exact date and time for the service</li>
                <li>💬 Discuss any final details or requirements</li>
                <li>✅ Prepare for your service</li>
            </ul>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View My Bookings</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting You with Quality Services</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_CANCELLED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .alert {{ color: #e74c3c; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #e74c3c; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Booking Cancelled</h1>
        </div>
        <div class="content">
            <div class="alert">Your booking has been cancelled</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Cancelled Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Original Price:</span>
                        <span class="detail-value">R{service_price}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Cancellation Reason</h3>
                    <p>{cancellation_reason}</p>
                </div>
            </div>
           
            <p><strong>What you can do:</strong></p>
            <ul>
                <li>🔍 Search for other service providers</li>
                <li>📞 Contact us if you need assistance</li>
                <li>💬 Explore different service categories</li>
                <li>⭐ Find alternative businesses with good ratings</li>
            </ul>
           
            <p>We apologize for any inconvenience this may have caused.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Find Other Services</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting You with Quality Services</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_COMPLETED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #3498db; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #27ae60; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Service Completed!</h1>
        </div>
        <div class="content">
            <div class="success">Thank you for using our service!</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Service Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Service Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Amount:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
            </div>
           
            <p><strong>We hope you had a great experience!</strong></p>
            <ul>
                <li>⭐ Consider leaving a review for the business</li>
                <li>📞 Contact the business for any follow-up needs</li>
                <li>🔍 Explore more services on our platform</li>
                <li>💬 Share your experience with friends and family</li>
            </ul>
           
            <p>Thank you for choosing Business Connect for your service needs!</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Book More Services</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting You with Quality Services</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""



# Database Models


class User(db.Model):
    __tablename__ = "User"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_num = db.Column(db.String(50))
    user_type = db.Column(db.String(50))
    reg_date = db.Column(db.Date, default=db.func.current_date())

class BusinessOwner(db.Model):
    __tablename__ = "BusinessOwner"

    owner_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id", ondelete="CASCADE"))
    title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    bus_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    num_years = db.Column(db.String(50))

    user = db.relationship("User", backref="owner_profile", lazy=True)

class Service(db.Model):
    __tablename__ = "Service"

    service_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("BusinessOwner.owner_id", ondelete="CASCADE"))
    service_category = db.Column(db.String(255))
    range_price = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)

    owner = db.relationship("BusinessOwner", backref="services")
    categories = db.relationship("Category", backref="service", cascade="all, delete-orphan")
    images = db.relationship("Images", backref="service", cascade="all, delete-orphan")

class Category(db.Model):
    __tablename__ = "Category"

    category_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    category_type = db.Column(db.String(255))
    total_units = db.Column(db.Integer)
    amenities = db.Column(db.Text)

class Images(db.Model):
    __tablename__ = "Images"

    image_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    filename = db.Column(db.String(255), nullable=False)


class Booking(db.Model):
    __tablename__ = "Booking"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id", ondelete="CASCADE"))
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    booking_date = db.Column(db.Date, default=date.today)
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    special_request = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("bookings", lazy=True))
    service = db.relationship("Service", backref=db.backref("bookings", lazy=True))

    def update_status(self, new_status, welcome_message=""):
        """Update booking status and send email notification to customer"""
        old_status = self.status
        self.status = new_status
       
        # If approved and there's a welcome message, add it to special request
        if new_status == 'Approved' and welcome_message:
            current_request = self.special_request or ""
            self.special_request = f"{current_request}\n\n(Business Message:) {welcome_message}".strip()
       
        db.session.commit()
       
        # Send email notification to customer
        self.send_status_notification(old_status, new_status, welcome_message)
   
    def send_status_notification(self, old_status, new_status, welcome_message=""):
        """Send email notification to customer when booking status changes"""
        try:
            if new_status == "Approved":
                subject = "🎉 Booking Approved - Business Connect"
                email_html = BOOKING_APPROVED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    owner_name=f"{self.service.owner.user.name} {self.service.owner.user.surname}",
                    business_phone=self.service.owner.user.phone_num or "Contact via platform",
                    business_email=self.service.owner.user.email,
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    dashboard_url=url_for('view_my_bookings', customer_id=self.user.user_id, _external=True)
                )
            elif new_status == "Cancelled":
                subject = "❌ Booking Cancelled - Business Connect"
                email_html = BOOKING_CANCELLED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    owner_name=f"{self.service.owner.user.name} {self.service.owner.user.surname}",
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    cancellation_reason="The business owner has cancelled your booking",
                    dashboard_url=url_for('customer_dashboard', _external=True)
                )
            elif new_status == "Completed":
                subject = "✅ Service Completed - Business Connect"
                email_html = BOOKING_COMPLETED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    dashboard_url=url_for('customer_dashboard', _external=True)
                )
            else:
                return
           
            send_email(subject, self.user.email, email_html)
            print(f"✅ Status notification sent to {self.user.email}")
           
        except Exception as e:
            print(f"❌ Failed to send status notification: {e}")

app.config['UPLOAD_FOLDER'] = 'static/uploads'

def send_email(subject, recipient, html_body):
    """Send email function"""
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            html=html_body
        )
        mail.send(msg)
        print(f"✅ Email sent to: {recipient}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False



# ------------------- ROUTES -------------------
@app.route('/')
def home():
    return render_template('index.html')

#------------------RESET PASSSWORD-------------------
#------------------RESET PASSSWORD-------------------
#------------------RESET PASSSWORD-----------------

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not email or not new_password or not confirm_password:
            flash("All fields are required.", "error")
            return redirect(url_for('reset_password'))

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))

        # Check password strength (minimum 8 characters)
        if len(new_password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for('reset_password'))

        # Find user by email
        user = User.query.filter_by(email=email).first()
       
        if not user:
            # For security reasons, don't reveal if email exists or not
            flash("If your email exists in our system, a password reset has been processed.", "success")
            return redirect(url_for('login'))

        # Update password
        try:
            user.password = new_password
            db.session.commit()
           
            # Send password change confirmation email
            email_sent = send_password_change_email(user)
           
            if email_sent:
                flash("Password reset successfully! Confirmation email sent. You can now login with your new password.", "success")
            else:
                flash("Password reset successfully! However, confirmation email failed to send.", "warning")
           
            return redirect(url_for('login'))
           
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while resetting your password. Please try again.", "error")
            return redirect(url_for('reset_password'))

    # GET request - show reset password form
    return render_template('reset_password.html')

def send_password_change_email(user):
    """Send email notification when password is changed"""
    try:
        email_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
                .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
                .content {{ padding: 30px; }}
                .alert {{ background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
                .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-item {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #2c3e50; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Changed Successfully</h1>
                </div>
                <div class="content">
                    <div class="alert">
                        <strong>Security Notice:</strong> Your password has been updated
                    </div>
                   
                    <div class="details">
                        <h3>Account Security Update</h3>
                        <div class="detail-item">
                            <span class="label">Name:</span> {user.name} {user.surname}
                        </div>
                        <div class="detail-item">
                            <span class="label">Email:</span> {user.email}
                        </div>
                        <div class="detail-item">
                            <span class="label">New Password:</span> {user.password}
                        </div>
                        <div class="detail-item">
                            <span class="label">Time:</span> {date.today().strftime("%B %d, %Y %H:%M")}
                        </div>
                    </div>
                   
                    <p>Your Business Connect account password was successfully changed.</p>
                   
                    <p><strong>If you did not make this change:</strong></p>
                    <ul>
                        <li>Reset your password immediately using the forgot password feature</li>
                        <li>Contact our support team if you need assistance</li>
                        <li>Ensure your email account is secure</li>
                    </ul>
                   
                    <div class="footer">
                        <p><strong>Business Connect</strong> - Growing Together</p>
                        <p>&copy; 2025 Business Connect. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
       
        msg = Message(
            subject="Password Changed - Business Connect",
            recipients=[user.email],
            html=email_html
        )
        mail.send(msg)
        print(f"✅ Password change notification sent to: {user.email}")
        return True
       
    except Exception as e:
        print(f"❌ Failed to send password change email: {e}")
        return False
    """Send email notification when password is changed"""
    try:
        email_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
                .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
                .content {{ padding: 30px; }}
                .alert {{ background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
                .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-item {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #2c3e50; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Changed Successfully</h1>
                </div>
                <div class="content">
                    <div class="alert">
                        <strong>Security Notice:</strong> Your password has been updated
                    </div>
                   
                    <div class="details">
                        <h3>Account Security Update</h3>
                        <div class="detail-item">
                            <span class="label">Name:</span> {user.name} {user.surname}
                        </div>
                        <div class="detail-item">
                            <span class="label">Email:</span> {user.email}
                        </div>
                        <div class="detail-item">
                            <span class="label">Time:</span> {date.today().strftime("%B %d, %Y %H:%M")}
                        </div>
                    </div>
                   
                    <p>Your Business Connect account password was successfully changed.</p>
                   
                    <p><strong>If you did not make this change:</strong></p>
                    <ul>
                        <li>Reset your password immediately using the forgot password feature</li>
                        <li>Contact our support team if you need assistance</li>
                        <li>Ensure your email account is secure</li>
                    </ul>
                   
                    <div class="footer">
                        <p><strong>Business Connect</strong> - Growing Together</p>
                        <p>&copy; 2025 Business Connect. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
       
        msg = Message(
            subject="Password Changed - Business Connect",
            recipients=[user.email],
            html=email_html
        )
        mail.send(msg)
        print(f"✅ Password change notification sent to: {user.email}")
        return True
       
    except Exception as e:
        print(f"❌ Failed to send password change email: {e}")
        return False




@app.route('/services')
def services():
    return render_template('services.html')



@app.route('/listings')
def listings():
    return render_template('listings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.user_id
            session['user_type'] = user.user_type

            if user.user_type == "BusinessOwner":
                return redirect(url_for('businessowner_dashboard'))
            elif user.user_type == "Customer":
                return redirect(url_for('customer_dashboard'))
            elif user.user_type == "Admin":
                return redirect(url_for('admin_dashboard'))

        flash("Invalid login credentials", "error")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
       
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "error")
            return render_template('signup.html')
       
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            phone_num=phone_num,
            user_type=user_type,
        )
       
        db.session.add(new_user)
        db.session.commit()
       
        # Send welcome email
        welcome_html = WELCOME_EMAIL_HTML.format(
            name=f"{name} {surname}",
            email=email,
            user_type=user_type,
            phone=phone_num if phone_num else "Not provided",
            reg_date=new_user.reg_date.strftime("%B %d, %Y"),
            login_url=url_for('login', _external=True)
        )
       
        if send_email("Welcome to Business Connect!", email, welcome_html):
            flash("Account created successfully! Welcome email sent.", "success")
        else:
            flash("Account created successfully! Welcome email failed to send.", "warning")
       
        return redirect(url_for('signup_successful'))
   
    return render_template('signup.html')

@app.route('/signup_successful')
def signup_successful():
    return render_template('signup_successful.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
   
# Business Owner Routes
@app.route('/businessowner/dashboard')
def businessowner_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=user_id).first()
    user = User.query.get(user_id)

    return render_template('businessowner_dashboard.html', owner=owner, user=user)

@app.route('/register_business', methods=['GET', 'POST'])
def register_business():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        bus_type = request.form.get('bus_type')
        description = request.form.get('description')
        address = request.form.get('address')
        num_years = request.form.get('num_years')

        business = BusinessOwner(
            user_id=session['user_id'],
            title=title,
            location=location,
            bus_type=bus_type,
            description=description,
            address=address,
            num_years=num_years
        )

        db.session.add(business)
        db.session.commit()

        # Send business registration confirmation email to the owner
        user = User.query.get(session['user_id'])
        business_html = BUSINESS_REGISTRATION_HTML.format(
            title=title,
            location=location,
            bus_type=bus_type,
            address=address,
            num_years=num_years,
            dashboard_url=url_for('businessowner_dashboard', _external=True)
        )
       
        # Send notification to all users about new business
        notification_sent = send_new_business_notification(business, user)
       
        if send_email("Business Profile Registered - Business Connect", user.email, business_html) and notification_sent:
            flash("Business profile created successfully! Confirmation email sent and all users have been notified.", "success")
        elif send_email("Business Profile Registered - Business Connect", user.email, business_html):
            flash("Business profile created successfully! Confirmation email sent, but user notifications failed.", "warning")
        elif notification_sent:
            flash("Business profile created successfully! All users notified, but confirmation email failed.", "warning")
        else:
            flash("Business profile created successfully! But email notifications failed to send.", "warning")

        return redirect(url_for('businessowner_dashboard'))

    return render_template('register_business.html')

def send_new_business_notification(business, business_owner):
    """Send notification to all users when a new business is registered"""
    try:
        # Get all users (both customers and other business owners)
        all_users = User.query.all()
       
        if not all_users:
            print("❌ No users found to notify")
            return False
       
        print(f"📧 Preparing to notify {len(all_users)} users about new business...")
       
        success_count = 0
        fail_count = 0
       
        for user in all_users:
            # Skip sending notification to the business owner themselves
            if user.user_id == business_owner.user_id:
                continue
               
            email_html = NEW_BUSINESS_EMAIL_HTML.format(
                business_name=business.title,
                business_type=business.bus_type,
                business_location=business.location,
                owner_name=f"{business_owner.name} {business_owner.surname}",
                business_description=business.description or "Professional services available",
                years_experience=business.num_years or "Several",
                dashboard_url=url_for('view_businesses', _external=True)
            )
           
            subject = f"🏢 New Business Registered: {business.title} - Business Connect"
           
            if send_email(subject, user.email, email_html):
                success_count += 1
            else:
                fail_count += 1
       
        print(f"✅ New business notification completed: {success_count} successful, {fail_count} failed")
        return success_count > 0
       
    except Exception as e:
        print(f"❌ Error in send_new_business_notification: {e}")
        return False

@app.route('/edit_business_profile', methods=['GET', 'POST'])
def edit_business_profile():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not business:
        return redirect(url_for('register_business'))

    if request.method == 'POST':
        business.title = request.form.get('title')
        business.location = request.form.get('location')
        business.bus_type = request.form.get('bus_type')
        business.description = request.form.get('description')
        business.address = request.form.get('address')
        business.num_years = request.form.get('num_years')

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('businessowner_dashboard'))

    return render_template('edit_business_profile.html', business=business)

@app.route('/delete_business_profile')
def delete_business_profile():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if business:
        db.session.delete(business)
        db.session.commit()
        flash("Business Profile deleted successfully!", "success")
    else:
        flash("No business profile found to delete.", "error")

    return redirect(url_for('businessowner_dashboard'))

@app.route('/manage_services', methods=['GET', 'POST'])
def manage_services():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not business:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=business.owner_id).all()
    return render_template('manage_services.html', business=business, services=services)


@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()

    if request.method == 'POST':
        category = request.form.get('service_category')
        price = request.form.get('range_price')

        new_service = Service(
            owner_id=business.owner_id,
            service_category=category,
            range_price=price
        )
        db.session.add(new_service)
        db.session.commit()

        flash("Service added successfully!", "success")
        return redirect(url_for('manage_services'))

    return render_template('add_service.html')
 

@app.route('/delete_service/<int:service_id>')
def delete_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('manage_services'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner or service.owner_id != owner.owner_id:
        flash("You do not have permission to delete this service.", "error")
        return redirect(url_for('manage_services'))

    db.session.delete(service)
    db.session.commit()
    flash("Service and all linked info successfully deleted!", "success")
    return redirect(url_for('manage_services'))

@app.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service:
        flash("Service not found", "error")
        return redirect(url_for('manage_services'))

    if request.method == 'POST':
        service.service_category = request.form.get('service_category')
        service.range_price = request.form.get('range_price')
        service.is_active = bool(request.form.get('is_active'))

        db.session.commit()
        flash("Service updated successfully", "success")
        return redirect(url_for('manage_services'))

    return render_template("edit_service.html", service=service)

@app.route('/manage_category')
def manage_category():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=owner.owner_id).all()
    return render_template('manage_category.html', services=services)

@app.route('/add_image/<int:service_id>', methods=['POST'])
def add_image(service_id):
    service = Service.query.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('manage_category'))

    image_count = Images.query.filter_by(service_id=service_id).count()
    if image_count >= 3:
        flash("Maximum 3 images allowed for each category.", "error")
        return redirect(url_for('manage_category'))

    if 'image_file' not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for('manage_category'))

    file = request.files['image_file']
    if file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('manage_category'))

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_img = Images(service_id=service_id, filename=filename)
    db.session.add(new_img)
    db.session.commit()

    flash("Image uploaded successfully!", "success")
    return redirect(url_for('manage_category'))

@app.route('/delete_image/<int:image_id>')
def delete_image(image_id):
    img = Images.query.get(image_id)
    if not img:
        flash("Image not found.", "error")
        return redirect(url_for('manage_category'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(img)
    db.session.commit()

    flash("Image deleted successfully!", "success")
    return redirect(url_for('manage_category'))

@app.route('/view_services')
def view_services():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=owner.owner_id).all()
    return render_template('view_services.html', services=services)

@app.route('/businessowner/bookings')
def view_bookings():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))
   
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))
   
    # Get all bookings for this business owner's services
    bookings = db.session.query(Booking, Service, User).\
        join(Service, Booking.service_id == Service.service_id).\
        join(User, Booking.user_id == User.user_id).\
        filter(Service.owner_id == owner.owner_id).\
        order_by(Booking.booking_date.desc()).all()
   
    return render_template('business_bookings.html', bookings=bookings, owner=owner)

@app.route('/businessowner/update_booking_status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))
   
    booking = Booking.query.get_or_404(booking_id)
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
   
    # Verify this booking belongs to the business owner
    if booking.service.owner_id != owner.owner_id:
        flash("You don't have permission to update this booking.", "error")
        return redirect(url_for('view_bookings'))
   
    new_status = request.form.get('status')
    welcome_message = request.form.get('welcome_message', '')
   
    if new_status:
        # Use the update_status method which handles email notifications
        booking.update_status(new_status, welcome_message)
        flash("Booking status updated successfully! Customer has been notified via email.", "success")
   
    return redirect(url_for('view_bookings'))



#----------------------------- Customer Routes -----------------------------
#----------------------------- Customer Routes -----------------------------
#----------------------------- Customer Routes -----------------------------

@app.route("/customer/dashboard")
def customer_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Customer":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    services = Service.query.filter_by(is_active=True).all()
   
    # Get all business owners
    owners = {}
    for service in services:
        if service.owner_id not in owners:
            owner = BusinessOwner.query.get(service.owner_id)
            if owner:
                owners[service.owner_id] = {
                    'owner': owner,
                    'user': User.query.get(owner.user_id)
                }
   
    return render_template("customer_dashboard.html", user=user, services=services, owners=owners)

@app.route("/customer/view_services/<int:owner_id>")
def customer_view_services(owner_id):
    owner = BusinessOwner.query.get_or_404(owner_id)
    services = Service.query.filter_by(owner_id=owner_id).all()
    return render_template("customer_view_services.html", owner=owner, services=services)





@app.route("/customer/booking/success")
def booking_success():
    return render_template("booking_success.html")

@app.route("/customer/book/<int:service_id>", methods=["GET", "POST"])
def customer_book(service_id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    service = Service.query.get(service_id)

    if not service:
        return "Service not found", 404

    owner = service.owner

    if request.method == "POST":
        special_request = request.form.get("special_request")

        # Create booking
        booking = Booking(
            user_id=user.user_id,
            service_id=service.service_id,
            total_amount=service.range_price,
            status="Pending",
            special_request=special_request
        )
        db.session.add(booking)
        db.session.commit()

        # Prepare special request HTML
        special_request_html = ""
        if special_request:
            special_request_html = f"""
            <div class="special-request">
                <h4>Special Request from Customer:</h4>
                <p>"{special_request}"</p>
            </div>
            """

        # Send email to owner
        owner_html = BOOKING_NOTIFICATION_HTML.format(
            service_category=service.service_category,
            service_price=service.range_price,
            customer_name=f"{user.name} {user.surname}",
            customer_email=user.email,
            customer_phone=user.phone_num if user.phone_num else "Not provided",
            booking_date=booking.booking_date.strftime("%B %d, %Y"),
            special_request_html=special_request_html,
            dashboard_url=url_for('businessowner_dashboard', _external=True)
        )

        # Send email to customer
        customer_html = BOOKING_CONFIRMATION_HTML.format(
            service_category=service.service_category,
            business_name=owner.title if owner.title else f"{owner.user.name}'s Business",
            owner_name=f"{owner.user.name} {owner.user.surname}",
            service_price=service.range_price,
            business_phone=owner.user.phone_num if owner.user.phone_num else "Contact via platform",
            business_email=owner.user.email,
            booking_date=booking.booking_date.strftime("%B %d, %Y"),
            special_request_html=special_request_html,
            dashboard_url=url_for('view_my_bookings', customer_id=user.user_id, _external=True)
        )

        # Send both emails
        owner_email_sent = send_email("New Booking Received - Business Connect", owner.user.email, owner_html)
        customer_email_sent = send_email("Booking Sent- Business Connect", user.email, customer_html)

        if owner_email_sent and customer_email_sent:
            flash("Booking confirmed! Beautiful confirmation emails have been sent to both you and the business owner.", "success")
        elif owner_email_sent:
            flash("Booking confirmed! Email sent to business owner, but failed to send confirmation to you.", "warning")
        elif customer_email_sent:
            flash("Booking confirmed! Confirmation email sent to you, but failed to notify business owner.", "warning")
        else:
            flash("Booking confirmed! However, email notifications failed to send.", "warning")

        return redirect(url_for("booking_success"))

    return render_template("confirm_booking.html", user=user, service=service, owner=owner)

@app.route("/customer/cancel_booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status != "Pending":
        flash("Only pending bookings can be cancelled.", "warning")
    else:
        booking.status = "Cancelled"
        db.session.commit()
        flash("Booking cancelled successfully.", "success")
           
    return redirect(url_for("view_my_bookings", customer_id=session["user_id"]))

@app.route("/customer/businesses")
def view_businesses():
    businesses = BusinessOwner.query.join(Service).filter(Service.is_active == True).all()
    return render_template("view_businesses.html", businesses=businesses)

@app.route("/customer/bookings/<int:customer_id>")
def view_my_bookings(customer_id):
    user = User.query.get(customer_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    bookings = Booking.query.filter_by(user_id=customer_id).all()
    return render_template("my_bookings.html", bookings=bookings, user=user)


   






#------------------ADMIN ROUTES-------------------
#------------------ADMIN ROUTES-------------------
#------------------ADMIN ROUTES-------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    # Get counts for dashboard
    business_owners_count = User.query.filter_by(user_type='BusinessOwner').count()
    customers_count = User.query.filter_by(user_type='Customer').count()
    services_count = Service.query.count()
    businesses_count = BusinessOwner.query.count()
   
    return render_template('admin_dashboard.html',
                         business_owners_count=business_owners_count,
                         customers_count=customers_count,
                         services_count=services_count,
                         businesses_count=businesses_count)

@app.route('/admin/add-owner', methods=['GET', 'POST'])
def admin_add_owner():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
       
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for('admin_add_owner'))
       
        # Create new business owner
        new_owner = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            phone_num=phone_num,
            user_type="BusinessOwner",
        )
       
        db.session.add(new_owner)
        db.session.commit()
       
        flash("Business owner added successfully!", "success")
        return redirect(url_for('admin_dashboard'))
   
    return render_template('addowner.html')

@app.route('/admin/view-businesses')
def admin_view_businesses():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    businesses = BusinessOwner.query.all()
    return render_template('admin_businesses.html', businesses=businesses)

@app.route('/admin/view-services')
def admin_view_services():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    services = Service.query.all()
    return render_template('admin_services.html', services=services)

@app.route('/admin/view-business-owners')
def admin_view_business_owners():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    business_owners = User.query.filter_by(user_type='BusinessOwner').all()
    return render_template('admin_business_owners.html', business_owners=business_owners)

@app.route('/admin/view-customers')
def admin_view_customers():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    customers = User.query.filter_by(user_type='Customer').all()
    return render_template('admin_customers.html', customers=customers)

@app.route('/admin/delete-user/<int:user_id>')
def admin_delete_user(user_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    user = User.query.get(user_id)
    if user:
        # Delete associated business profile if exists
        business_profile = BusinessOwner.query.filter_by(user_id=user_id).first()
        if business_profile:
            db.session.delete(business_profile)
       
        # Delete associated services
        services = Service.query.filter_by(owner_id=user_id).all()
        for service in services:
            db.session.delete(service)
       
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found.", "error")
   
    return redirect(request.referrer or url_for('admin_dashboard'))

@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin_dashboard'))
   
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.email = request.form.get('email')
        user.phone_num = request.form.get('phone_num')
       
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('admin_view_' + ('business_owners' if user.user_type == 'BusinessOwner' else 'customers')))
   
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/delete-service/<int:service_id>')
def admin_delete_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash("Service deleted successfully!", "success")
    else:
        flash("Service not found.", "error")
   
    return redirect(url_for('admin_view_services'))

@app.route('/admin/delete-business/<int:business_id>')
def admin_delete_business(business_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    business = BusinessOwner.query.get(business_id)
    if business:
        db.session.delete(business)
        db.session.commit()
        flash("Business profile deleted successfully!", "success")
    else:
        flash("Business profile not found.", "error")
   
    return redirect(url_for('admin_view_businesses'))



    # ------------------- logout -------------------from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from datetime import date
from flask import request
import os
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

load_dotenv()  # Load .env values if running locally

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")  # Always keep secret key safe

# Setup Flask-Mail with corrected configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'businessconnectrsa@gmail.com'
app.config['MAIL_PASSWORD'] = 'upytpexovucqaiqx'  # Using app password
app.config['MAIL_DEFAULT_SENDER'] = 'businessconnectrsa@gmail.com'

mail = Mail(app)

# --------------- DATABASE CONFIG -----------------
# Try to get hosted DB URL (e.g., from Railway / Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

# If no hosted DB found, use local DB
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
<<<<<<< Updated upstream
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin2023@localhost:5432/businessconnect"
=======
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Maxelo%402023@localhost:5432/businessconnect"
>>>>>>> Stashed changes

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Fixed Email Templates with escaped curly braces
WELCOME_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #27ae60; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Business Connect! 🎉</h1>
        </div>
        <div class="content">
            <div class="success">Your Account is Ready!</div>
           
            <div class="details">
                <h3>Account Details:</h3>
                <div class="detail-item"><span class="label">Name:</span> {name}</div>
                <div class="detail-item"><span class="label">Email:</span> {email}</div>
                <div class="detail-item"><span class="label">User Type:</span> {user_type}</div>
                <div class="detail-item"><span class="label">Phone:</span> {phone}</div>
                <div class="detail-item"><span class="label">Registration Date:</span> {reg_date}</div>
            </div>
           
            <p>Thank you for joining Business Connect! We're excited to have you on board.</p>
           
            <div style="text-align: center;">
                <a href="{login_url}" class="button">Login to Your Account</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BUSINESS_REGISTRATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Business Profile Registered! ✅</h1>
        </div>
        <div class="content">
            <div class="success">Your Business is Live!</div>
           
            <div class="details">
                <h3>Business Details:</h3>
                <div class="detail-item"><span class="label">Business Name:</span> {title}</div>
                <div class="detail-item"><span class="label">Location:</span> {location}</div>
                <div class="detail-item"><span class="label">Business Type:</span> {bus_type}</div>
                <div class="detail-item"><span class="label">Address:</span> {address}</div>
                <div class="detail-item"><span class="label">Years in Business:</span> {num_years}</div>
            </div>
           
            <p>Your business profile has been successfully registered on Business Connect!</p>
            <p>You can now start adding services and accepting bookings from customers.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Go to Business Dashboard</a>
            </div>
           
            <div class="footer">
                 <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_NOTIFICATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .alert {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .special-request {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 15px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Booking Received! 🎉</h1>
        </div>
        <div class="content">
            <div class="alert">
                <h2>You Have a New Booking!</h2>
                <p>A customer has booked your service</p>
            </div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Service Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service Category:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Customer Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Name:</span>
                        <span class="detail-value">{customer_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">{customer_email}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Phone:</span>
                        <span class="detail-value">{customer_phone}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Booking Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Status:</span>
                        <span class="detail-value" style="color: #f39c12; font-weight: bold;">Pending Confirmation</span>
                    </div>
                </div>
            </div>
           
            {special_request_html}
           
            <p><strong>Action Required:</strong> Please contact the customer within 24 hours to confirm this booking.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View Booking in Dashboard</a>
            </div>
           
            <div class="footer">
               
                <p>This is an automated notification. Please do not reply to this email.</p>

                 <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
NEW_BUSINESS_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .announcement {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .business-details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #9b59b6; }}
        .detail-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; }}
        .owner-info {{ background: #e8f6f3; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 New Business Joined!</h1>
        </div>
        <div class="content">
            <div class="announcement">
                <h2>Exciting News!</h2>
                <p>A new business has joined Business Connect</p>
            </div>
           
            <div class="business-details">
                <h3>🎯 Business Information</h3>
                <div class="detail-item">
                    <span class="label">Business Name:</span>
                    <span>{business_name}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Business Type:</span>
                    <span>{business_type}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Location:</span>
                    <span>{business_location}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Stated in:</span>
                    <span>{years_experience} </span>
                </div>
                <div class="detail-item">
                    <span class="label">Description:</span>
                    <span>{business_description}</span>
                </div>
            </div>
           
            <div class="owner-info">
                <h3>👤 Business Owner</h3>
                <div class="detail-item">
                    <span class="label">Owner Name:</span>
                    <span>{owner_name}</span>
                </div>
            </div>
           
            <p><strong>What this means for you:</strong></p>
            <ul>
                <li>✅ More service options available</li>
                <li>✅ Increased competition for better prices</li>
                <li>✅ Expanded network of professionals</li>
                <li>✅ More choices for your needs</li>
            </ul>
           
            <p>Check out their services and see what they have to offer!</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">📋 View All Businesses</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_CONFIRMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .special-request {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 15px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Booking Sent! ✅</h1>
        </div>
        <div class="content">
            <div class="success">Your Booking is Sent!</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Contact Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Business Phone:</span>
                        <span class="detail-value">{business_phone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business Email:</span>
                        <span class="detail-value">{business_email}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                   
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
            </div>
           
            {special_request_html}
           
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>The business owner will contact you within 48 hours</li>
                <li>You can view your booking status in your dashboard</li>
                <li>Prepare any necessary information for the service</li>
            </ul>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View My Bookings</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
           
                <p>&copy; 2025 Business Connect. All rights reserved.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_APPROVED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #27ae60 0%, #219653 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #27ae60; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Booking Approved!</h1>
        </div>
        <div class="content">
            <div class="success">Great News! Your booking has been approved</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Price:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Contact Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Business Phone:</span>
                        <span class="detail-value">{business_phone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business Email:</span>
                        <span class="detail-value">{business_email}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Next Steps</h3>
                    <p>The business owner will contact you shortly to arrange the service details.</p>
                    <p>Please keep your phone available and check your messages regularly.</p>
                </div>
            </div>
           
            <p><strong>What to expect next:</strong></p>
            <ul>
                <li>📞 The business owner will contact you within 48 hours</li>
                <li>📅 Schedule the exact date and time for the service</li>
                <li>💬 Discuss any final details or requirements</li>
                <li>✅ Prepare for your service</li>
            </ul>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">View My Bookings</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_CANCELLED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .alert {{ color: #e74c3c; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #e74c3c; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Booking Cancelled</h1>
        </div>
        <div class="content">
            <div class="alert">Your booking has been cancelled</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Cancelled Booking Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Owner:</span>
                        <span class="detail-value">{owner_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Original Price:</span>
                        <span class="detail-value">R{service_price}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Booking Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                </div>
               
                <div class="detail-section">
                    <h3>Cancellation Reason</h3>
                    <p>{cancellation_reason}</p>
                </div>
            </div>
           
            <p><strong>What you can do:</strong></p>
            <ul>
                <li>🔍 Search for other service providers</li>
                <li>📞 Contact us if you need assistance</li>
                <li>💬 Explore different service categories</li>
               
            </ul>
           
            <p>We apologize for any inconvenience this may have caused.</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Find Other Services</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

BOOKING_COMPLETED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .header {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
        .content {{ padding: 30px; }}
        .success {{ color: #3498db; font-size: 24px; text-align: center; margin: 20px 0; }}
        .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ font-weight: bold; color: #2c3e50; }}
        .detail-value {{ color: #34495e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #27ae60; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Service Completed!</h1>
        </div>
        <div class="content">
            <div class="success">Thank you for using our service!</div>
           
            <div class="details">
                <div class="detail-section">
                    <h3>Service Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Service:</span>
                        <span class="detail-value">{service_category}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Business:</span>
                        <span class="detail-value">{business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Service Date:</span>
                        <span class="detail-value">{booking_date}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Amount:</span>
                        <span class="detail-value" style="color: #27ae60; font-weight: bold;">R{service_price}</span>
                    </div>
                </div>
            </div>
           
            <p><strong>We hope you had a great experience!</strong></p>
            <ul>
               
                <li>📞 Contact the business for any follow-up needs</li>
                <li>🔍 Explore more services on our platform</li>
                <li>💬 Share your experience with friends and family</li>
            </ul>
           
            <p>Thank you for choosing Business Connect for your service needs!</p>
           
            <div style="text-align: center;">
                <a href="{dashboard_url}" class="button">Book More Services</a>
            </div>
           
            <div class="footer">
                <p><strong>Business Connect</strong> - Connecting Services With Dignity</p>
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""



# Database Models


class User(db.Model):
    __tablename__ = "User"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_num = db.Column(db.String(50))
    user_type = db.Column(db.String(50))
    reg_date = db.Column(db.Date, default=db.func.current_date())

class BusinessOwner(db.Model):
    __tablename__ = "BusinessOwner"

    owner_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id", ondelete="CASCADE"))
    title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    bus_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    num_years = db.Column(db.String(50))

    user = db.relationship("User", backref="owner_profile", lazy=True)

class Service(db.Model):
    __tablename__ = "Service"

    service_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("BusinessOwner.owner_id", ondelete="CASCADE"))
    service_category = db.Column(db.String(255))
    range_price = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)

    owner = db.relationship("BusinessOwner", backref="services")
    categories = db.relationship("Category", backref="service", cascade="all, delete-orphan")
    images = db.relationship("Images", backref="service", cascade="all, delete-orphan")

class Category(db.Model):
    __tablename__ = "Category"

    category_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    category_type = db.Column(db.String(255))
    total_units = db.Column(db.Integer)
    amenities = db.Column(db.Text)

class Images(db.Model):
    __tablename__ = "Images"

    image_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    filename = db.Column(db.String(255), nullable=False)


class Booking(db.Model):
    __tablename__ = "Booking"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id", ondelete="CASCADE"))
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    booking_date = db.Column(db.Date, default=date.today)
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    special_request = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("bookings", lazy=True))
    service = db.relationship("Service", backref=db.backref("bookings", lazy=True))

    def update_status(self, new_status, welcome_message=""):
        """Update booking status and send email notification to customer"""
        old_status = self.status
        self.status = new_status
       
        # If approved and there's a welcome message, add it to special request
        if new_status == 'Approved' and welcome_message:
            current_request = self.special_request or ""
            self.special_request = f"{current_request}\n\n(Business Message:) {welcome_message}".strip()
       
        db.session.commit()
       
        # Send email notification to customer
        self.send_status_notification(old_status, new_status, welcome_message)
   
    def send_status_notification(self, old_status, new_status, welcome_message=""):
        """Send email notification to customer when booking status changes"""
        try:
            if new_status == "Approved":
                subject = "🎉 Booking Approved - Business Connect"
                email_html = BOOKING_APPROVED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    owner_name=f"{self.service.owner.user.name} {self.service.owner.user.surname}",
                    business_phone=self.service.owner.user.phone_num or "Contact via platform",
                    business_email=self.service.owner.user.email,
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    dashboard_url=url_for('view_my_bookings', customer_id=self.user.user_id, _external=True)
                )
            elif new_status == "Cancelled":
                subject = "❌ Booking Cancelled - Business Connect"
                email_html = BOOKING_CANCELLED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    owner_name=f"{self.service.owner.user.name} {self.service.owner.user.surname}",
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    cancellation_reason="The business owner has cancelled your booking",
                    dashboard_url=url_for('customer_dashboard', _external=True)
                )
            elif new_status == "Completed":
                subject = "✅ Service Completed - Business Connect"
                email_html = BOOKING_COMPLETED_HTML.format(
                    customer_name=f"{self.user.name} {self.user.surname}",
                    service_category=self.service.service_category,
                    business_name=self.service.owner.title if hasattr(self.service.owner, 'title') else f"{self.service.owner.user.name}'s Business",
                    booking_date=self.booking_date.strftime("%B %d, %Y"),
                    service_price=self.service.range_price,
                    dashboard_url=url_for('customer_dashboard', _external=True)
                )
            else:
                return
           
            send_email(subject, self.user.email, email_html)
            print(f"✅ Status notification sent to {self.user.email}")
           
        except Exception as e:
            print(f"❌ Failed to send status notification: {e}")

app.config['UPLOAD_FOLDER'] = 'static/uploads'

def send_email(subject, recipient, html_body):
    """Send email function"""
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            html=html_body
        )
        mail.send(msg)
        print(f"✅ Email sent to: {recipient}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False



# ------------------- ROUTES -------------------
@app.route('/')
def home():
    return render_template('index.html')

#------------------RESET PASSSWORD-------------------
#------------------RESET PASSSWORD-------------------
#------------------RESET PASSSWORD-----------------

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not email or not new_password or not confirm_password:
            flash("All fields are required.", "error")
            return redirect(url_for('reset_password'))

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))

        # Check password strength (minimum 8 characters)
        if len(new_password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for('reset_password'))

        # Find user by email
        user = User.query.filter_by(email=email).first()
       
        if not user:
            # For security reasons, don't reveal if email exists or not
            flash("If your email exists in our system, a password reset has been processed.", "success")
            return redirect(url_for('login'))

        # Update password
        try:
            user.password = new_password
            db.session.commit()
           
            # Send password change confirmation email
            send_password_change_email(user)
           
            flash("Password reset successfully! You can now login with your new password.", "success")
            return redirect(url_for('login'))
           
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while resetting your password. Please try again.", "error")
            return redirect(url_for('reset_password'))

    # GET request - show reset password form
    return render_template('reset_password.html')

def send_password_change_email(user):
    """Send email notification when password is changed"""
    try:
        email_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
                .header {{ background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
                .content {{ padding: 30px; }}
                .alert {{ background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
                .details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .detail-item {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #2c3e50; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Changed Successfully</h1>
                </div>
                <div class="content">
                    <div class="alert">
                        <strong>Security Notice:</strong> Your password has been updated
                    </div>
                   
                    <div class="details">
                        <h3>Account Security Update</h3>
                        <div class="detail-item">
                            <span class="label">Name:</span> {user.name} {user.surname}
                        </div>
                        <div class="detail-item">
                            <span class="label">Email:</span> {user.email}
                        </div>
                        <div class="detail-item">
                            <span class="label">New Password:</span> {user.password}
                        </div>
                        <div class="detail-item">
                            <span class="label">Time:</span> {date.today().strftime("%B %d, %Y %H:%M")}
                        </div>
                    </div>
                   
                    <p>Your Business Connect account password was successfully changed.</p>
                   
                    <p><strong>If you did not make this change:</strong></p>
                    <ul>
                        <li>Reset your password immediately using the forgot password feature</li>
                        <li>Contact our support team if you need assistance</li>
                        <li>Ensure your email account is secure</li>
                    </ul>
                   
                    <div class="footer">
                        <p><strong>Business Connect</strong> - Growing Together</p>
                        <p>&copy; 2025 Business Connect. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
       
        msg = Message(
            subject="Password Changed - Business Connect",
            recipients=[user.email],
            html=email_html
        )
        mail.send(msg)
        print(f"✅ Password change notification sent to: {user.email}")
        return True
       
    except Exception as e:
        print(f"❌ Failed to send password change email: {e}")
        return False




@app.route('/services')
def services():
    return render_template('services.html')



@app.route('/listings')
def listings():
    return render_template('listings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.user_id
            session['user_type'] = user.user_type

            if user.user_type == "BusinessOwner":
                return redirect(url_for('businessowner_dashboard'))
            elif user.user_type == "Customer":
                return redirect(url_for('customer_dashboard'))
            elif user.user_type == "Admin":
                return redirect(url_for('admin_dashboard'))

        flash("Invalid login credentials", "error")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
       
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "error")
            return render_template('signup.html')
       
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            phone_num=phone_num,
            user_type=user_type,
        )
       
        db.session.add(new_user)
        db.session.commit()
       
        # Send welcome email
        welcome_html = WELCOME_EMAIL_HTML.format(
            name=f"{name} {surname}",
            email=email,
            user_type=user_type,
            phone=phone_num if phone_num else "Not provided",
            reg_date=new_user.reg_date.strftime("%B %d, %Y"),
            login_url=url_for('login', _external=True)
        )
       
        if send_email("Welcome to Business Connect!", email, welcome_html):
            flash("Account created successfully! Welcome email sent.", "success")
        else:
            flash("Account created successfully! Welcome email failed to send.", "warning")
       
        return redirect(url_for('signup_successful'))
   
    return render_template('signup.html')

@app.route('/signup_successful')
def signup_successful():
    return render_template('signup_successful.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
   
# Business Owner Routes
@app.route('/businessowner/dashboard')
def businessowner_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=user_id).first()
    user = User.query.get(user_id)

    return render_template('businessowner_dashboard.html', owner=owner, user=user)

@app.route('/register_business', methods=['GET', 'POST'])
def register_business():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        bus_type = request.form.get('bus_type')
        description = request.form.get('description')
        address = request.form.get('address')
        num_years = request.form.get('num_years')

        business = BusinessOwner(
            user_id=session['user_id'],
            title=title,
            location=location,
            bus_type=bus_type,
            description=description,
            address=address,
            num_years=num_years
        )

        db.session.add(business)
        db.session.commit()

        # Send business registration confirmation email to the owner
        user = User.query.get(session['user_id'])
        business_html = BUSINESS_REGISTRATION_HTML.format(
            title=title,
            location=location,
            bus_type=bus_type,
            address=address,
            num_years=num_years,
            dashboard_url=url_for('businessowner_dashboard', _external=True)
        )
       
        # Send notification to all users about new business
        notification_sent = send_new_business_notification(business, user)
       
        if send_email("Business Profile Registered - Business Connect", user.email, business_html) and notification_sent:
            flash("Business profile created successfully! Confirmation email sent and all users have been notified.", "success")
        elif send_email("Business Profile Registered - Business Connect", user.email, business_html):
            flash("Business profile created successfully! Confirmation email sent, but user notifications failed.", "warning")
        elif notification_sent:
            flash("Business profile created successfully! All users notified, but confirmation email failed.", "warning")
        else:
            flash("Business profile created successfully! But email notifications failed to send.", "warning")

        return redirect(url_for('businessowner_dashboard'))

    return render_template('register_business.html')

def send_new_business_notification(business, business_owner):
    """Send notification to all users when a new business is registered"""
    try:
        # Get all users (both customers and other business owners)
        all_users = User.query.all()
       
        if not all_users:
            print("❌ No users found to notify")
            return False
       
        print(f"📧 Preparing to notify {len(all_users)} users about new business...")
       
        success_count = 0
        fail_count = 0
       
        for user in all_users:
            # Skip sending notification to the business owner themselves
            if user.user_id == business_owner.user_id:
                continue
               
            email_html = NEW_BUSINESS_EMAIL_HTML.format(
                business_name=business.title,
                business_type=business.bus_type,
                business_location=business.location,
                owner_name=f"{business_owner.name} {business_owner.surname}",
                business_description=business.description or "Professional services available",
                years_experience=business.num_years or "Several",
                dashboard_url=url_for('view_businesses', _external=True)
            )
           
            subject = f"🏢 New Business Registered: {business.title} - Business Connect"
           
            if send_email(subject, user.email, email_html):
                success_count += 1
            else:
                fail_count += 1
       
        print(f"✅ New business notification completed: {success_count} successful, {fail_count} failed")
        return success_count > 0
       
    except Exception as e:
        print(f"❌ Error in send_new_business_notification: {e}")
        return False

@app.route('/edit_business_profile', methods=['GET', 'POST'])
def edit_business_profile():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not business:
        return redirect(url_for('register_business'))

    if request.method == 'POST':
        business.title = request.form.get('title')
        business.location = request.form.get('location')
        business.bus_type = request.form.get('bus_type')
        business.description = request.form.get('description')
        business.address = request.form.get('address')
        business.num_years = request.form.get('num_years')

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('businessowner_dashboard'))

    return render_template('edit_business_profile.html', business=business)

@app.route('/delete_business_profile')
def delete_business_profile():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if business:
        db.session.delete(business)
        db.session.commit()
        flash("Business Profile deleted successfully!", "success")
    else:
        flash("No business profile found to delete.", "error")

    return redirect(url_for('businessowner_dashboard'))

@app.route('/manage_services', methods=['GET', 'POST'])
def manage_services():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not business:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=business.owner_id).all()
    return render_template('manage_services.html', business=business, services=services)


@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()

    if request.method == 'POST':
        category = request.form.get('service_category')
        price = request.form.get('range_price')

        new_service = Service(
            owner_id=business.owner_id,
            service_category=category,
            range_price=price
        )
        db.session.add(new_service)
        db.session.commit()

        flash("Service added successfully!", "success")
        return redirect(url_for('manage_services'))

    return render_template('add_service.html')
 

@app.route('/delete_service/<int:service_id>')
def delete_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('manage_services'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner or service.owner_id != owner.owner_id:
        flash("You do not have permission to delete this service.", "error")
        return redirect(url_for('manage_services'))

    db.session.delete(service)
    db.session.commit()
    flash("Service and all linked info successfully deleted!", "success")
    return redirect(url_for('manage_services'))

@app.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    service = Service.query.get(service_id)
    if not service:
        flash("Service not found", "error")
        return redirect(url_for('manage_services'))

    if request.method == 'POST':
        service.service_category = request.form.get('service_category')
        service.range_price = request.form.get('range_price')
        service.is_active = bool(request.form.get('is_active'))

        db.session.commit()
        flash("Service updated successfully", "success")
        return redirect(url_for('manage_services'))

    return render_template("edit_service.html", service=service)

@app.route('/manage_category')
def manage_category():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=owner.owner_id).all()
    return render_template('manage_category.html', services=services)

@app.route('/add_image/<int:service_id>', methods=['POST'])
def add_image(service_id):
    service = Service.query.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('manage_category'))

    image_count = Images.query.filter_by(service_id=service_id).count()
    if image_count >= 3:
        flash("Maximum 3 images allowed for each category.", "error")
        return redirect(url_for('manage_category'))

    if 'image_file' not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for('manage_category'))

    file = request.files['image_file']
    if file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('manage_category'))

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_img = Images(service_id=service_id, filename=filename)
    db.session.add(new_img)
    db.session.commit()

    flash("Image uploaded successfully!", "success")
    return redirect(url_for('manage_category'))

@app.route('/delete_image/<int:image_id>')
def delete_image(image_id):
    img = Images.query.get(image_id)
    if not img:
        flash("Image not found.", "error")
        return redirect(url_for('manage_category'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(img)
    db.session.commit()

    flash("Image deleted successfully!", "success")
    return redirect(url_for('manage_category'))

@app.route('/view_services')
def view_services():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    services = Service.query.filter_by(owner_id=owner.owner_id).all()
    return render_template('view_services.html', services=services)

@app.route('/businessowner/bookings')
def view_bookings():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))
   
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))
   
    # Get all bookings for this business owner's services
    bookings = db.session.query(Booking, Service, User).\
        join(Service, Booking.service_id == Service.service_id).\
        join(User, Booking.user_id == User.user_id).\
        filter(Service.owner_id == owner.owner_id).\
        order_by(Booking.booking_date.desc()).all()
   
    return render_template('business_bookings.html', bookings=bookings, owner=owner)

@app.route('/businessowner/update_booking_status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))
   
    booking = Booking.query.get_or_404(booking_id)
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
   
    # Verify this booking belongs to the business owner
    if booking.service.owner_id != owner.owner_id:
        flash("You don't have permission to update this booking.", "error")
        return redirect(url_for('view_bookings'))
   
    new_status = request.form.get('status')
    welcome_message = request.form.get('welcome_message', '')
   
    if new_status:
        # Use the update_status method which handles email notifications
        booking.update_status(new_status, welcome_message)
        flash("Booking status updated successfully! Customer has been notified via email.", "success")
   
    return redirect(url_for('view_bookings'))



#----------------------------- Customer Routes -----------------------------
#----------------------------- Customer Routes -----------------------------
#----------------------------- Customer Routes -----------------------------

@app.route("/customer/dashboard")
def customer_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Customer":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    services = Service.query.filter_by(is_active=True).all()

    return render_template("customer_dashboard.html", user=user, services=services)

@app.route("/customer/view_services/<int:owner_id>")
def customer_view_services(owner_id):
    owner = BusinessOwner.query.get_or_404(owner_id)
    services = Service.query.filter_by(owner_id=owner_id).all()
    return render_template("customer_view_services.html", owner=owner, services=services)

@app.route("/customer/booking/success")
def booking_success():
    return render_template("booking_success.html")

@app.route("/customer/book/<int:service_id>", methods=["GET", "POST"])
def customer_book(service_id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    service = Service.query.get(service_id)

    if not service:
        return "Service not found", 404

    owner = service.owner

    if request.method == "POST":
        special_request = request.form.get("special_request")

        # Create booking
        booking = Booking(
            user_id=user.user_id,
            service_id=service.service_id,
            total_amount=service.range_price,
            status="Pending",
            special_request=special_request
        )
        db.session.add(booking)
        db.session.commit()

        # Prepare special request HTML
        special_request_html = ""
        if special_request:
            special_request_html = f"""
            <div class="special-request">
                <h4>Special Request from Customer:</h4>
                <p>"{special_request}"</p>
            </div>
            """

        # Send email to owner
        owner_html = BOOKING_NOTIFICATION_HTML.format(
            service_category=service.service_category,
            service_price=service.range_price,
            customer_name=f"{user.name} {user.surname}",
            customer_email=user.email,
            customer_phone=user.phone_num if user.phone_num else "Not provided",
            booking_date=booking.booking_date.strftime("%B %d, %Y"),
            special_request_html=special_request_html,
            dashboard_url=url_for('businessowner_dashboard', _external=True)
        )

        # Send email to customer
        customer_html = BOOKING_CONFIRMATION_HTML.format(
            service_category=service.service_category,
            business_name=owner.title if owner.title else f"{owner.user.name}'s Business",
            owner_name=f"{owner.user.name} {owner.user.surname}",
            service_price=service.range_price,
            business_phone=owner.user.phone_num if owner.user.phone_num else "Contact via platform",
            business_email=owner.user.email,
            booking_date=booking.booking_date.strftime("%B %d, %Y"),
            special_request_html=special_request_html,
            dashboard_url=url_for('view_my_bookings', customer_id=user.user_id, _external=True)
        )

        # Send both emails
        owner_email_sent = send_email("New Booking Received - Business Connect", owner.user.email, owner_html)
        customer_email_sent = send_email("Booking Sent- Business Connect", user.email, customer_html)

        if owner_email_sent and customer_email_sent:
            flash("Booking confirmed! Beautiful confirmation emails have been sent to both you and the business owner.", "success")
        elif owner_email_sent:
            flash("Booking confirmed! Email sent to business owner, but failed to send confirmation to you.", "warning")
        elif customer_email_sent:
            flash("Booking confirmed! Confirmation email sent to you, but failed to notify business owner.", "warning")
        else:
            flash("Booking confirmed! However, email notifications failed to send.", "warning")

        return redirect(url_for("booking_success"))

    return render_template("confirm_booking.html", user=user, service=service, owner=owner)

@app.route("/customer/cancel_booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status != "Pending":
        flash("Only pending bookings can be cancelled.", "warning")
    else:
        booking.status = "Cancelled"
        db.session.commit()
        flash("Booking cancelled successfully.", "success")
           
    return redirect(url_for("view_my_bookings", customer_id=session["user_id"]))

@app.route("/customer/businesses")
def view_businesses():
    businesses = BusinessOwner.query.join(Service).filter(Service.is_active == True).all()
    return render_template("view_businesses.html", businesses=businesses)

@app.route("/customer/bookings/<int:customer_id>")
def view_my_bookings(customer_id):
    user = User.query.get(customer_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    bookings = Booking.query.filter_by(user_id=customer_id).all()
    return render_template("my_bookings.html", bookings=bookings, user=user)






#------------------ADMIN ROUTES-------------------
#------------------ADMIN ROUTES-------------------
#------------------ADMIN ROUTES-------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    # Get counts for dashboard
    business_owners_count = User.query.filter_by(user_type='BusinessOwner').count()
    customers_count = User.query.filter_by(user_type='Customer').count()
    services_count = Service.query.count()
    businesses_count = BusinessOwner.query.count()
   
    return render_template('admin_dashboard.html',
                         business_owners_count=business_owners_count,
                         customers_count=customers_count,
                         services_count=services_count,
                         businesses_count=businesses_count)

@app.route('/admin/add-owner', methods=['GET', 'POST'])
def admin_add_owner():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
       
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for('admin_add_owner'))
       
        # Create new business owner
        new_owner = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            phone_num=phone_num,
            user_type="BusinessOwner",
        )
       
        db.session.add(new_owner)
        db.session.commit()
       
        flash("Business owner added successfully!", "success")
        return redirect(url_for('admin_dashboard'))
   
    return render_template('addowner.html')

@app.route('/admin/view-businesses')
def admin_view_businesses():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    businesses = BusinessOwner.query.all()
    return render_template('admin_businesses.html', businesses=businesses)

@app.route('/admin/view-services')
def admin_view_services():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    services = Service.query.all()
    return render_template('admin_services.html', services=services)

@app.route('/admin/view-business-owners')
def admin_view_business_owners():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    business_owners = User.query.filter_by(user_type='BusinessOwner').all()
    return render_template('admin_business_owners.html', business_owners=business_owners)

@app.route('/admin/view-customers')
def admin_view_customers():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    customers = User.query.filter_by(user_type='Customer').all()
    return render_template('admin_customers.html', customers=customers)

@app.route('/admin/delete-user/<int:user_id>')
def admin_delete_user(user_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    user = User.query.get(user_id)
    if user:
        # Delete associated business profile if exists
        business_profile = BusinessOwner.query.filter_by(user_id=user_id).first()
        if business_profile:
            db.session.delete(business_profile)
       
        # Delete associated services
        services = Service.query.filter_by(owner_id=user_id).all()
        for service in services:
            db.session.delete(service)
       
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found.", "error")
   
    return redirect(request.referrer or url_for('admin_dashboard'))

@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin_dashboard'))
   
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.email = request.form.get('email')
        user.phone_num = request.form.get('phone_num')
       
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('admin_view_' + ('business_owners' if user.user_type == 'BusinessOwner' else 'customers')))
   
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/delete-service/<int:service_id>')
def admin_delete_service(service_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash("Service deleted successfully!", "success")
    else:
        flash("Service not found.", "error")
   
    return redirect(url_for('admin_view_services'))

@app.route('/admin/delete-business/<int:business_id>')
def admin_delete_business(business_id):
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
   
    business = BusinessOwner.query.get(business_id)
    if business:
        db.session.delete(business)
        db.session.commit()
        flash("Business profile deleted successfully!", "success")
    else:
        flash("Business profile not found.", "error")
   
    return redirect(url_for('admin_view_businesses'))


<<<<<<< Updated upstream
# ------------------- LOGOUT -------------------
=======

    # ------------------- logout -------------------
    # -------------------LOGOUT-------------------
>>>>>>> Stashed changes
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

# ------------------- RUN SERVER -------------------
<<<<<<< Updated upstream
from waitress import serve
import os
=======
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    # -------------------LOGOUT-------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))
>>>>>>> Stashed changes

if __name__ == '__main__':
<<<<<<< Updated upstream
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))
    serve(app, host='0.0.0.0', port=port)
=======
    with app.app_context():
        db.create_all()
>>>>>>> Stashed changes
