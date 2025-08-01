# app2.py
# This file contains the Flask application for handling customer signup

from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# RDS credentials
DB_HOST = "customerdb.cqde0qymciac.us-east-1.rds.amazonaws.com"
DB_NAME = "customerdata"
DB_USER = "dbadmin"
DB_PASS = "p057Gr3$QL"

# Route: Page 1 - Public Info Signup
@app.route('/signup-step1', methods=['GET', 'POST'])
def signup_step1():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form['date'] or None  # Accept empty string as NULL
        state = request.form['state']
        city = request.form['city']
        hospital = request.form['hospital']
        doctor = request.form['doctor']
        notes = request.form['notes']

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

# Route: Page 2 - Private Info Signup
@app.route('/signup-step2', methods=['GET', 'POST'])
def signup_step2():
    public_id = request.args.get('public_id')
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name')  # Optional
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

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