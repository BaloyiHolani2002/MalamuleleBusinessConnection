from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env values if running locally

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_here")  # Always keep secret key safe

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
    accommodations = db.relationship("Accommodation", backref="service", cascade="all, delete-orphan")
    images = db.relationship("Images", backref="service", cascade="all, delete-orphan")


class Accommodation(db.Model):
    __tablename__ = "Accommodation"

    accom_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    accom_type = db.Column(db.String(255))
    total_rooms = db.Column(db.Integer)
    amenities = db.Column(db.Text)

    # Rooms relationship
    rooms = db.relationship("Room", backref="accommodation", cascade="all, delete-orphan")


class Images(db.Model):
    __tablename__ = "Images"

    image_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.service_id", ondelete="CASCADE"))
    image_url = db.Column(db.Text)


class Room(db.Model):
    __tablename__ = "Room"

    room_id = db.Column(db.Integer, primary_key=True)
    accom_id = db.Column(db.Integer, db.ForeignKey("Accommodation.accom_id", ondelete="CASCADE"))
    room_type = db.Column(db.String(255))
    room_num = db.Column(db.Integer)
    avail_status = db.Column(db.String(50))
    price_per_night = db.Column(db.String(50))


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




# ------------------- RUN SERVER -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Creates tables if not exist
    app.run(debug=True)
