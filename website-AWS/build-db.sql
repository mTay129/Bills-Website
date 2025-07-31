-- Create database (you may need to do this from the RDS console or your DB admin tool)
-- CREATE DATABASE customerdata;

-- Switch to the correct database in your client (pgAdmin, psql, etc.)
-- \c customerdata;

-- Table: Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    first_name BYTEA NOT NULL,
    middle_name BYTEA,  -- Optional encrypted middle name
    last_name BYTEA NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    billing_address TEXT NOT NULL
);

-- Table: Birth Details (public information)
CREATE TABLE IF NOT EXISTS public_info (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    date INTEGER,  -- Optional day of birth
    state VARCHAR(100),
    city VARCHAR(100),
    hospital VARCHAR(255),
    doctor_or_midwife VARCHAR(255),
    notes VARCHAR(10)
);

-- Table: Private Info (contact info linked to public info)
CREATE TABLE IF NOT EXISTS private_info (
    id SERIAL PRIMARY KEY,
    public_info_id INTEGER REFERENCES public_info(id) ON DELETE CASCADE,
    first_name BYTEA NOT NULL,
    middle_name BYTEA,
    last_name BYTEA NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    billing_address TEXT NOT NULL
);

-- (Optional) Table: Sales Tax (if used elsewhere)
CREATE TABLE IF NOT EXISTS sales_tax (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(50),
    sales_tax_rate DECIMAL(5,2)
);
