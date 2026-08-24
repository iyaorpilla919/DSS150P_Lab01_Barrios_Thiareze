-- CREATE SCHEMA
CREATE SCHEMA IF NOT EXISTS lab;

-- CREATE TARGET TABLE FOR CUSTOMERS
CREATE TABLE IF NOT EXISTS lab.customers (
    customer_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    city TEXT,
    signup_date DATE,
    customer_segment TEXT NOT NULL,
    CONSTRAINT ck_customer_id_format CHECK (customer_id ~ '^C[0-9]+$')
);