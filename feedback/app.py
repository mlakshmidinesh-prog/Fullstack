from flask import Flask, render_template, request, redirect, url_for
from repository.feedback_repository import save_feedback

app = Flask(__name__)

# 1. Route to show the form
@app.route("/", methods=["GET"])
def feedback_page():
    return render_template("feedback.html")

# 2. Route to process the form data
@app.route('/submit', methods=['POST'])
def submit():
    # Capture the data sent from the HTML form
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Call your repository function to save the details to MySQL
    if name and email and message:
        save_feedback(name, email, message)
        # Use redirect to move to the success page
        return redirect(url_for('success_page'))
    
    return "Error: Missing form fields", 400

# 3. Route to show the success message
@app.route("/success", methods=["GET"])
def success_page():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)