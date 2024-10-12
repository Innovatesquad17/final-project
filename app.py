from flask import Flask, render_template, request, redirect, session, url_for, flash
import pandas as pd
from model import recommend_internships  # Import the model
from users import is_user_registered, register_user, validate_login  # User authentication functions

app = Flask(__name__)
app.secret_key = 'suhaina@%123'

# Paths to CSV files
internship_data_path = r"C:\Users\Admin\Desktop\internship_data.csv"
student_data_path = r"C:\Users\Admin\Desktop\Student_data.csv"

# Load the internship data, handle encoding issues
try:
    internships = pd.read_csv(internship_data_path, encoding='ISO-8859-1')
except UnicodeDecodeError:
    internships = pd.read_csv(internship_data_path, encoding='utf-16')


# Route for home/login page
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        skills = request.form['skills']
        location = request.form['location']

        # Check if the user exists
        if validate_login(email):
            session['email'] = email
            session['skills'] = skills
            session['location'] = location
            return redirect(url_for('recommend'))
        else:
            flash('User not found. Please register first.')
            return redirect(url_for('register'))

    return render_template('index.html')


# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']

        # Check if the email is already registered
        if is_user_registered(email):
            flash('Email already registered. Please log in.')
            return redirect(url_for('index'))

        # Collect other user data for registration
        student_data = [
            request.form['name'],
            request.form['institution'],
            request.form['category'],
            request.form['email'],
            request.form['contact'],
            request.form['gender'],
            request.form['area_of_interest'],
            request.form['nationality'],
            request.form['physically_handicapped'],
            request.form['academic_qualifications'],
            request.form['preferred_locations'],
            request.form['skills'],
            request.form['languages_known']
        ]

        # Register the user
        register_user(student_data)
        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    return render_template('register.html')


# Route for internship recommendation
@app.route('/recommend')
def recommend():
    if 'email' not in session:
        flash('Please log in to view recommendations.')
        return redirect(url_for('index'))

    skills = session['skills']
    location = session['location']

    # Call the recommendation logic from the model
    recommended_internships = recommend_internships(internships, skills, location)

    return render_template('recommendation.html', internships=recommended_internships)


if __name__ == '__main__':
    app.run(debug=True)
