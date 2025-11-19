from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from datetime import date
import os
from dotenv import load_dotenv
import re

load_dotenv()  # Load .env values if running locally

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'businessconnectrsa@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'businessconnectrsa@gmail.com'

mail = Mail(app)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for Render's PostgreSQL URL format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Use Render database or fallback to local
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin2023@localhost:5432/businessconnect"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email Templates
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

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not email or not new_password or not confirm_password:
            flash("All fields are required.", "error")
            return redirect(url_for('reset_password'))

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))

        if len(new_password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for('reset_password'))

        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("If your email exists in our system, a password reset has been processed.", "success")
            return redirect(url_for('login'))

        try:
            user.password = new_password
            db.session.commit()
            flash("Password reset successfully! You can now login with your new password.", "success")
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while resetting your password. Please try again.", "error")
            return redirect(url_for('reset_password'))

    return render_template('reset_password.html')

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
        
        welcome_html = WELCOME_EMAIL_HTML.format(
            name=f"{name} {surname}",
            email=email,
            user_type=user_type,
            phone=phone_num if phone_num else "Not provided",
            reg_date=new_user.reg_date.strftime("%B %d, %Y"),
            login_url=url_for('login', _external=True)
        )
        
     #   if send_email("Welcome to Business Connect!", email, welcome_html):
      #      flash("Account created successfully! Welcome email sent.", "success")
       # else:
       #     flash("Account created successfully! Welcome email failed to send.", "warning")
        
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

        user = User.query.get(session['user_id'])
        business_html = BUSINESS_REGISTRATION_HTML.format(
            title=title,
            location=location,
            bus_type=bus_type,
            address=address,
            num_years=num_years,
            dashboard_url=url_for('businessowner_dashboard', _external=True)
        )
        
        # if send_email("Business Profile Registered - Business Connect", user.email, business_html):
        #    flash("Business profile created successfully! Confirmation email sent.", "success")
        #else:
        #    flash("Business profile created successfully! But confirmation email failed to send.", "warning")

        return redirect(url_for('businessowner_dashboard'))

    return render_template('register_business.html')

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
    
    bookings = db.session.query(Booking, Service, User).\
        join(Service, Booking.service_id == Service.service_id).\
        join(User, Booking.user_id == User.user_id).\
        filter(Service.owner_id == owner.owner_id).\
        order_by(Booking.booking_date.desc()).all()
    
    return render_template('business_bookings.html', bookings=bookings, owner=owner)

# Customer Routes
@app.route("/customer/dashboard")
def customer_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Customer":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    services = Service.query.filter_by(is_active=True).all()
    
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

        booking = Booking(
            user_id=user.user_id,
            service_id=service.service_id,
            total_amount=service.range_price,
            status="Pending",
            special_request=special_request
        )
        db.session.add(booking)
        db.session.commit()

        special_request_html = ""
        if special_request:
            special_request_html = f"""
            <div class="special-request">
                <h4>Special Request from Customer:</h4>
                <p>"{special_request}"</p>
            </div>
            """

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

       # owner_email_sent = send_email("New Booking Received - Business Connect", owner.user.email, owner_html)
       # customer_email_sent = send_email("Booking Sent- Business Connect", user.email, customer_html)

       # if owner_email_sent and customer_email_sent:
       #     flash("Booking confirmed! Beautiful confirmation emails have been sent to both you and the business owner.", "success")
       # elif owner_email_sent:
       #     flash("Booking confirmed! Email sent to business owner, but failed to send confirmation to you.", "warning")
       # elif customer_email_sent:
       #     flash("Booking confirmed! Confirmation email sent to you, but failed to notify business owner.", "warning")
       # else:
       #     flash("Booking confirmed! However, email notifications failed to send.", "warning")

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

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_type') != "Admin":
        return redirect(url_for('login'))
    
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
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for('admin_add_owner'))
        
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
        business_profile = BusinessOwner.query.filter_by(user_id=user_id).first()
        if business_profile:
            db.session.delete(business_profile)
        
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

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # For production on Render
    if os.getenv("RENDER"):
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(debug=True)
