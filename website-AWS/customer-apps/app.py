# app.py
# This file contains the Flask application for handling customer signup

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import re
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# Database credentials
DB_HOST = "customerdb.cqde0qymciac.us-east-1.rds.amazonaws.com"
DB_NAME = "customerdata"
DB_USER = "dbadmin"
DB_PASS = "p057Gr3$QL"

# Load encryption key (replace with environment variable in production)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

# Route: Page 1 - Public Info Signup
@app.route('/signup-step1', methods=['GET', 'POST'])
def signup_step1():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form.get('date') or None  # Optional day
        state = request.form['state']
        city = request.form['city']
        hospital = request.form['hospital']
        doctor = request.form['doctor']
        notes = request.form['notes']

        # Validate inputs
        if not re.fullmatch(r"[A-Za-z\s]+", state): return "Invalid state"
        if not re.fullmatch(r"[A-Za-z\s]+", city): return "Invalid city"
        if not re.fullmatch(r"[A-Za-z\s]+", hospital): return "Invalid hospital"
        if not re.fullmatch(r"[A-Za-z\s]+", doctor): return "Invalid doctor"
        if len(notes) > 10: return "Notes must be under 10 characters"

        try:
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO public_info (year, month, date, state, city, hospital, doctor_or_midwife, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (year, month, date, state.strip(), city.strip(), hospital.strip(), doctor.strip(), notes.strip()))
            public_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('signup_step2', public_id=public_id))
        except Exception as e:
            return f"Error inserting public info: {str(e)}"

    return render_template('signup1.html')

# Route: Page 2 - Private Info Signup
@app.route('/signup-step2', methods=['GET', 'POST'])
def signup_step2():
    public_id = request.args.get('public_id')
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name') or None
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone'].replace('-', '')  # Remove hyphens
        address = request.form['address']

        # Validate names
        if not re.fullmatch(r"[A-Za-z\s]+", first_name): return "Invalid first name"
        if middle_name and not re.fullmatch(r"[A-Za-z\s]+", middle_name): return "Invalid middle name"
        if not re.fullmatch(r"[A-Za-z\s]+", last_name): return "Invalid last name"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): return "Invalid email format"
        if not re.fullmatch(r"[0-9]{10}", phone): return "Phone number must be 10 digits (hyphens are allowed but removed)"
        if not re.fullmatch(r"[A-Za-z0-9\s,.\-]+", address): return "Invalid address format"

        try:
            # Encrypt sensitive name fields
            enc_first = fernet.encrypt(first_name.strip().encode())
            enc_middle = fernet.encrypt(middle_name.strip().encode()) if middle_name else None
            enc_last = fernet.encrypt(last_name.strip().encode())

            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO private_info (public_info_id, first_name, middle_name, last_name, email, phone, billing_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (public_id, enc_first, enc_middle, enc_last, email.strip(), phone, address.strip()))
            conn.commit()
            cur.close()
            conn.close()
            return "Signup complete! Thank you."
        except Exception as e:
            return f"Error inserting private info: {str(e)}"

    return render_template('signup2.html', public_id=public_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
