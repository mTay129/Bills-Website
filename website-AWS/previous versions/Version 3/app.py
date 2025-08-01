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
    return render_template('home.html', active_page='home')

# Route: Page 2 - Public Info Signup
@app.route('/signup-step1', methods=['GET', 'POST'])
def signup_step1():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form.get('date') or None  # Optional

        state = request.form.get('state', '').strip()
        if not state:
            return "State is required."
        if not re.fullmatch(r"[A-Za-z\s]+", state):
            return "Invalid state value."

        city = request.form.get('city', '').strip() or None  # Optional
        if city and not re.fullmatch(r"[A-Za-z\s]+", city):
            return "Invalid city value."

        hospital = request.form.get('hospital', '').strip() or None  # Optional
        if hospital and not re.fullmatch(r"[A-Za-z\s]+", hospital):
                return "Invalid hospital value."

        doctor = request.form.get('doctor', '').strip() or None
        if doctor and not re.fullmatch(r"[A-Za-z\s]+", doctor):
            return "Invalid doctor or midwife value."

        notes = request.form.get('notes', '')  # Keep as string for length check
        if len(notes) > 10:
            return "Error: Notes must be 10 characters or fewer."
        notes = notes.strip()

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
            return render_template('signup1.html', error_message=str(e), active_page='signup')

    return render_template('signup1.html', error_message="", active_page='signup')

# Route: Page 2 cont. - Private Info Signup
@app.route('/signup-step2', methods=['GET', 'POST'])
def signup_step2():
    public_id = request.args.get('public_id')
    if not public_id:
        return redirect(url_for('signup_step1'))

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
            return render_template('signup2.html', public_id=public_id, success=True)
        except Exception as e:
            return render_template('signup2.html', public_id=public_id, error_message=str(e), success=False, active_page='signup')

    return render_template('signup2.html', public_id=public_id, error_message="", active_page='signup')

# Route: Privacy Policy Page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html', active_page='privacy')

# Route: Terms and Conditions Page
@app.route('/terms')
def terms():
    return render_template('terms.html', active_page='terms')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)