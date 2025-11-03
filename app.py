from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta, date
import psycopg2
import os
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=7)

# Simple password hashing (without bcrypt)
def hash_password(password):
    """Simple password hashing using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"

def check_password(hashed_password, user_password):
    """Check if the provided password matches the hashed password"""
    try:
        salt, original_hash = hashed_password.split('$')
        new_hash = hashlib.sha256((salt + user_password).encode()).hexdigest()
        return new_hash == original_hash
    except:
        return False

# Database initialization
def init_db():
    try:
        # Connect to default PostgreSQL database to create our database 
        default_conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Admin123"
        )
        default_conn.autocommit = True
        default_cur = default_conn.cursor()
        
        # Check if database exists, create one if not exists
        default_cur.execute("SELECT 1 FROM pg_database WHERE datname = 'businessconnect'")
        exists = default_cur.fetchone()
        
        if not exists:
            default_cur.execute("CREATE DATABASE businessconnect")
            print("Database successfully created")

        default_cur.close()
        default_conn.close()

        # Now connect to our database and create tables
        conn = get_db_connection()
        cur = conn.cursor()

        # Create tables    
        cur.execute("""
        CREATE TABLE IF NOT EXISTS "User" (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone_num VARCHAR(50),
            user_type VARCHAR(50),
            reg_date DATE DEFAULT CURRENT_DATE
        )
        """)

        # Create other tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS BusinessOwner (
            owner_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES "User"(user_id) ON DELETE CASCADE,
            title VARCHAR(255),
            location VARCHAR(255),
            bus_type VARCHAR(100),
            description TEXT,
            address VARCHAR(255),
            num_years VARCHAR(50)
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Service (
            service_id SERIAL PRIMARY KEY,
            owner_id INT REFERENCES BusinessOwner(owner_id) ON DELETE CASCADE,
            service_category VARCHAR(255),
            range_price DOUBLE PRECISION,
            is_active BOOLEAN DEFAULT TRUE
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Accommodation (
            accom_id SERIAL PRIMARY KEY,
            service_id INT REFERENCES Service(service_id) ON DELETE CASCADE,
            accom_type VARCHAR(255),
            total_rooms INT,
            amenities TEXT
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Images (
            image_id SERIAL PRIMARY KEY,
            service_id INT REFERENCES Service(service_id) ON DELETE CASCADE,
            image_url TEXT
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Room (
            room_id SERIAL PRIMARY KEY,
            accom_id INT REFERENCES Accommodation(accom_id) ON DELETE CASCADE,
            room_type VARCHAR(255),
            room_num INT,
            avail_status VARCHAR(50),
            price_per_night VARCHAR(50)
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Booking (
            booking_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES "User"(user_id) ON DELETE CASCADE,
            room_id INT REFERENCES Room(room_id) ON DELETE CASCADE,
            booking_date DATE DEFAULT CURRENT_DATE,
            check_in_date DATE,
            check_out_date DATE,
            total_amount DOUBLE PRECISION,
            total_guest INT,
            status VARCHAR(50),
            special_request TEXT
        )
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Notification (
            notification_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES "User"(user_id) ON DELETE CASCADE,
            title VARCHAR(255),
            message TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_date DATE DEFAULT CURRENT_DATE,
            notif_type VARCHAR(50)
        )
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Tables successfully created")

    except Exception as e:
        print(f"Error initializing database: {e}")

# Database connection
def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # If running locally
    if not DATABASE_URL:
        DATABASE_URL = "postgresql://postgres:Admin123@localhost:5432/businessconnect"

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

    try: 
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        # Return a connection to default database if businessconnect doesn't exist
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="Admin123"
            )
            return conn
        except:
            print("Could not connect to any database")
            return None

# Initialize the database when the app starts
with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Database connection failed', 'error')
                return render_template('login.html')
                
            cur = conn.cursor()
            
            cur.execute('SELECT * FROM "User" WHERE email = %s', (email,))
            user = cur.fetchone()
            
            if user and check_password(user[4], password):  # user[4] is password field
                session.permanent = bool(remember_me)
                session['user_id'] = user[0]  # user[0] is user_id
                session['email'] = user[3]    # user[3] is email
                session['name'] = user[1]     # user[1] is name
                session['user_type'] = user[6] # user[6] is user_type
                
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'error')
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        user_type = request.form.get('user_type', 'customer')  # Default to customer
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        
        # Basic validation
        if not all([name, surname, email, password, confirm_password]):
            flash('Please fill in all required fields', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('signup.html')
        
        try:
            conn = get_db_connection()
            if conn is None:
                flash('Database connection failed', 'error')
                return render_template('signup.html')
                
            cur = conn.cursor()
            
            # Check if email already exists
            cur.execute('SELECT user_id FROM "User" WHERE email = %s', (email,))
            if cur.fetchone():
                flash('Email already exists. Please use a different email.', 'error')
                return render_template('signup.html')
            
            # Hash password and insert user
            hashed_password = hash_password(password)
            cur.execute("""
                INSERT INTO "User" (name, surname, email, password, phone_num, user_type) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, surname, email, hashed_password, phone_num, user_type))
            
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Signup error: {e}")
            flash('An error occurred during registration', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

# API route for AJAX login
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Please fill in all fields'})
        
        conn = get_db_connection()
        if conn is None:
            return jsonify({'success': False, 'message': 'Database connection failed'})
            
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        user = cur.fetchone()
        
        if user and check_password(user[4], password):
            session['user_id'] = user[0]
            session['email'] = user[3]
            session['name'] = user[1]
            session['user_type'] = user[6]
            
            return jsonify({
                'success': True, 
                'message': 'Login successful!',
                'user': {
                    'name': user[1],
                    'email': user[3],
                    'user_type': user[6]
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'})
            
    except Exception as e:
        print(f"API login error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during login'})
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)