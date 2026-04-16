from flask import Flask, render_template, request
from repository.payment_repository import process_payment

app = Flask(__name__)

@app.route('/')
def home():
    return '<h2>Welcome!</h2><a href="/payment">Go to Payment Page </a>'

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    message = ""
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        merchant_id = int(request.form['merchant_id'])
        amount = float(request.form['amount'])
        message = process_payment(user_id, merchant_id, amount)
    return render_template('payment.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
