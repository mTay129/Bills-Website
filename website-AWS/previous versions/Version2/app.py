# app.py
# This file contains the Flask application for handling customer signup

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import re
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# RDS credentials
DB_HOST = "customerdb.cqde0qymciac.us-east-1.rds.amazonaws.com"
DB_NAME = "customerdata"
DB_USER = "dbadmin"
DB_PASS = "p057Gr3$QL"

# Route: Page 1 Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Route: Page 2 - Privacy Policy Page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Route: Page 3 - Terms and Conditions Page
@app.route('/terms')
def terms():
    return render_template('terms.html')


# Route: Page 4 - Public Info Signup
@app.route('/signup-step1', methods=['GET', 'POST'])
def signup_step1():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form.get('date') or None  # Allows blank value to become NULL in the database
        state = request.form['state']
        if not re.fullmatch(r"[A-Za-z\s]+", state):
            return "Invalid state value."
        state = state.strip()  # Remove leading/trailing spaces
        if not state:
            return "State is required."
        city = request.form['city']
        if not re.fullmatch(r"[A-Za-z\s]+", city):
            return "Invalid city value."
        city = city.strip()  # Remove leading/trailing spaces
        hospital = request.form['hospital']
        if not re.fullmatch(r"[A-Za-z\s]+", hospital):
            return "Invalid hospital value."
        hospital = hospital.strip()  # Remove leading/trailing spaces
        doctor = request.form['doctor']
        if not re.fullmatch(r"[A-Za-z\s]+", doctor):
            return "Invalid doctor or midwife value."
        doctor = doctor.strip()  # Remove leading/trailing spaces
        notes = request.form['notes']
        # Validate date input
        if len(notes) > 10:
            return "Error: Notes must be 10 characters or fewer."
        notes = notes.strip()  # Remove leading/trailing spaces
        
        try:
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO public_info (year, month, date, state, city, hospital, doctor_or_midwife, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (year, month, date, state, city, hospital, doctor, notes))
            public_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('signup_step2', public_id=public_id))
        except Exception as e:
            return f"Error inserting public info: {str(e)}"

    return render_template('signup1.html')

# Route: Page 4 cont. - Private Info Signup
@app.route('/signup-step2', methods=['GET', 'POST'])
def signup_step2():
    public_id = request.args.get('public_id')
    if request.method == 'POST':
        first_name = request.form['first_name']
        if not re.fullmatch(r"[A-Za-z\s]+", first_name):
            return "Invalid first name."
        first_name = first_name.strip()  # Remove leading/trailing spaces
        middle_name = request.form.get('middle_name')  # Optional
        if middle_name and not re.fullmatch(r"[A-Za-z\s]+", middle_name):
            return "Invalid middle name."
        middle_name = middle_name.strip() if middle_name else None  # Remove leading/trailing spaces
        last_name = request.form['last_name']
        if not re.fullmatch(r"[A-Za-z\s]+", last_name):
            return "Invalid last name."
        last_name = last_name.strip()  # Remove leading/trailing spaces
        email = request.form['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Simple email validation
            return "Invalid email format."
        email = email.strip()  # Remove leading/trailing spaces
        phone = request.form['phone']
        if not re.fullmatch(r"[0-9\-]{10,13}", phone):
            return "Invalid phone number. Only digits and hyphens allowed."
        phone = phone.strip()  # Remove leading/trailing spaces
        address = request.form['address']
        if not re.fullmatch(r"[A-Za-z0-9\s,.-]+", address):
            return "Invalid address format."
        address = address.strip()  # Remove leading/trailing spaces
        try:
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO private_info (
                    public_info_id, first_name, middle_name, last_name, email, phone, billing_address
                ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (public_id, first_name, middle_name, last_name, email, phone, address))
            conn.commit()
            cur.close()
            conn.close()
            return "Signup complete! Thank you."
        except Exception as e:
            return f"Error inserting private info: {str(e)}"

    return render_template('signup2.html', public_id=public_id)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)