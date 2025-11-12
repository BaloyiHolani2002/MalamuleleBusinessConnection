from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from datetime import date
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env values if running locally

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")  # Always keep secret key safe

# Setup Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or your email provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'timbearmindo191@gmail.com'
app.config['MAIL_PASSWORD'] = 'wjfgcpmyjqjoofrh'

mail = Mail(app)

# --------------- DATABASE CONFIG -----------------
# Try to get hosted DB URL (e.g., from Railway / Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# If no hosted DB found, use local DB
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin123@localhost:5432/businessconnect"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example Model (You can change later)
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

class User(db.Model):
    __tablename__ = "User"   # Must match the table name exactly

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

    # Relationships
    owner = db.relationship("BusinessOwner", backref="services")
   # owner = service.owner  # ✅ FIXED
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

    # Relationships
    user = db.relationship("User", backref=db.backref("bookings", lazy=True))
    service = db.relationship("Service", backref=db.backref("bookings", lazy=True))

    def __repr__(self):
        return f"<Booking {self.booking_id} | User {self.user_id} | Service {self.service_id}>"

app.config['UPLOAD_FOLDER'] = 'static/uploads'


# ------------------- HOME PAGE -------------------
@app.route('/')
def home():
    return render_template('index.html')


# ------------------- SERVICES PAGE -------------------
@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


# ------------------- LISTINGS PAGE -------------------
@app.route('/listings')
def listings():
    return render_template('listings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Check if user exists and password matches exactly
        if user and user.password == password:
            session['user_id'] = user.user_id
            session['user_type'] = user.user_type

            # Redirect based on user type
            if user.user_type == "BusinessOwner":
                return redirect(url_for('businessowner_dashboard'))

            elif user.user_type == "Customer":
                return redirect(url_for('customer_dashboard'))

            elif user.user_type == "Admin":
                return redirect(url_for('admin_dashboard'))

        flash("Invalid login credentials", "error")

    return render_template('login.html')

# ---- SIGNUP ROUTE ----
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        user_type = request.form.get('user_type')
        password = request.form.get('password')

        # Hash password
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "error")
            return render_template('signup.html')

        # Save new user
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            phone_num=phone_num,
            user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('signup_successful'))

    return render_template('signup.html')

# ---- SUCCESS PAGE ROUTE ----
@app.route('/signup_successful')
def signup_successful():
    return render_template('signup_successful.html')

# ------------------- ABOUT PAGE -------------------
@app.route('/about')
def about():
    return render_template('about.html')


# ------------------- CONTACT PAGE -------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("⚠️ All fields are required!", "error")
            return redirect(url_for('contact'))

        # Save into database
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash("✅ Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


# ------------------- BUSSINESS OWNER PAGE -------------------
# ------------------- BUSSINESS OWNER PAGE -------------------
@app.route('/businessowner/dashboard')
def businessowner_dashboard():
    user_id = session.get('user_id')

    # If not logged in → redirect
    if not user_id:
        return redirect(url_for('login'))

    # Fetch the logged-in BusinessOwner details
    owner = BusinessOwner.query.filter_by(user_id=user_id).first()

    # Fetch user details (Name, Email, etc.)
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

        return redirect(url_for('businessowner_dashboard'))

    return render_template('register_business.html')

@app.route('/edit_business_profile', methods=['GET', 'POST'])
def edit_business_profile():
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    # Get business owner linked to the logged-in user
    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()

    # If no business profile exists → send user to create one
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
    # Ensure logged in + correct user type
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    # Find linked business owner record
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

    # Get the business profile
    business = BusinessOwner.query.filter_by(user_id=session['user_id']).first()

    # If business not registered -> force profile creation
    if not business:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    # Fetch all services under this owner
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
    # Ensure logged in and role is BusinessOwner
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    # Get the service record
    service = Service.query.get(service_id)

    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('manage_services'))

    # Extra safety: ensure service belongs to this business owner
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner or service.owner_id != owner.owner_id:
        flash("You do not have permission to delete this service.", "error")
        return redirect(url_for('manage_services'))

    db.session.delete(service)
    db.session.commit()

    flash("Service and all linked info successfully deleted!", "success")
    return redirect(url_for('manage_services'))

    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully!", "success")
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

    # Limit to 3 images
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
    # Check if user is logged in
    if 'user_id' not in session or session.get('user_type') != "BusinessOwner":
        return redirect(url_for('login'))

    # Get business owner
    owner = BusinessOwner.query.filter_by(user_id=session['user_id']).first()
    if not owner:
        flash("Please register your business profile first.", "error")
        return redirect(url_for('register_business'))

    # Get all services for this owner
    services = Service.query.filter_by(owner_id=owner.owner_id).all()

    return render_template('view_services.html', services=services)


# ------------------- CUSTOMER DESHBOAD PAGE -------------------
# ------------------- CUSTOMER DESHBOAD PAGE -------------------

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

# --- Route to confirm booking page ---
@app.route("/customer/book/<int:service_id>", methods=["GET", "POST"])
def customer_book(service_id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    service = Service.query.get(service_id)

    if not service:
        return "Service not found", 404

    owner = service.owner  # BusinessOwner object

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

        # Send email to owner
        try:
            msg = Message(
                subject="New Booking Received",
                sender=app.config['MAIL_USERNAME'],
                recipients=[owner.user.email]  # Owner’s email
            )
            msg.body = f"""
Hello {owner.user.name},

You have a new booking!

Service: {service.service_category}
Customer: {user.name} {user.surname}
Phone: {user.phone_num}
Price: R{service.range_price}
Special Request: {special_request if special_request else 'None'}

Please check your dashboard for more details.
"""
            mail.send(msg)
        except Exception as e:
            print("Email send failed:", e)

        flash("Booking confirmed! An email has been sent to the owner.", "success")
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
    # Fetch all active businesses with their services
    businesses = BusinessOwner.query.join(Service).filter(Service.is_active == True).all()
    return render_template("view_businesses.html", businesses=businesses)

@app.route("/customer/bookings/<int:customer_id>")
def view_my_bookings(customer_id):
    # Fetch the user first
    user = User.query.get(customer_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    # Get all bookings for this user
    bookings = Booking.query.filter_by(user_id=customer_id).all()

    return render_template("my_bookings.html", bookings=bookings, user=user)

# ------------------- RUN SERVER -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Creates tables if not exist
    app.run(debug=True)
