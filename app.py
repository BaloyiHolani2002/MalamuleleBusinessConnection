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


# ------------------- RUN SERVER -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Creates tables if not exist
    app.run(debug=True)
