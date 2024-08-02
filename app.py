from flask import Flask, render_template, request, redirect, flash, session, url_for
import stripe


app = Flask(__name__, template_folder='template', static_folder='static')




YOUR_DOMAIN = 'http://127.0.0.1:5000'



stripe.api_key = "sk_test_51P3asWDifqfBQ4vNOQ7XLKTZLViJWv5zCygKTJck0aO8SvMO8aGTrAN5rc0brbuLYhNJdG7iPi8teySJWVfG05By00JNtjyhBl"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('tomi-tour_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
   

    return render_template('sign-in.html')

@app.route('/itenary')
def itenary():
    return render_template('itenary.html')

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
            success_url= '/booking',
            cancel_url= '/cancel.html'
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(debug=True)
