from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # change to something safe

# ------------------- HOME PAGE -------------------
@app.route('/')
def home():
    return render_template('index.html')

# ------------------- SERVICES PAGE -------------------
@app.route('/services')
def services():
    return render_template('services.html')

# ------------------- LISTINGS PAGE -------------------
@app.route('/listings')
def listings():
    return render_template('listings.html')

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

        # Check for empty fields
        if not name or not email or not message:
            flash("⚠️ All fields are required!", "error")
            return redirect(url_for('contact'))

        # Here you can store the message in a database later
        flash("✅ Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# ------------------- RUN SERVER -------------------
if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)