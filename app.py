from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
import requests
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import stripe
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='template', static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tomitour_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisismysecretkey'

db = SQLAlchemy(app)

YOUR_DOMAIN = 'http://127.0.0.1:5000'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

stripe.api_key = "sk_test_51P3asWDifqfBQ4vNOQ7XLKTZLViJWv5zCygKTJck0aO8SvMO8aGTrAN5rc0brbuLYhNJdG7iPi8teySJWVfG05By00JNtjyhBl"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('tomi-tour_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')


        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")

        # Prepare the data to be sent to PHP
        data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }

        # Send POST request to PHP script
        try:
            response = requests.post('http://localhost/TOMITOUR/tomi_db/register.php', data=data)
            response_data = response.json()

            if response_data['status'] == 'success':
                # Redirect to success page or any other page
                return redirect(url_for('home'))
            else:
                # Handle errors if needed
                flash(f"Error: {response_data['message']}", 'error')
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')

    return render_template('sign-in.html')

@app.route('/itenary')
def itenary():
    return render_template('itenary.html', user=current_user)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    return render_template('booking.html')

@app.route('/payment', methods=['POST'])
def payment():
    items = request.form.getlist('items')  
    quantities = request.form.getlist('quantities')  

    line_items = []
    for item, quantity in zip(items, quantities):
        line_items.append({
            'price': item,
            'quantity': int(quantity),
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url= YOUR_DOMAIN + '/booking',
            cancel_url= YOUR_DOMAIN + '/cancel.html'
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(debug=True)
