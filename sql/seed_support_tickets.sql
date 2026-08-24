CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    issue_category VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO support_tickets (customer_id, issue_category, status) VALUES
(101, 'Billing', 'Resolved'),
(102, 'Technical', 'Open'),
(103, 'Account Access', 'In Progress'),
(104, 'Billing', 'Open'),
(105, 'General Inquiry', 'Resolved');

CREATE TABLE IF NOT EXISTS inventory_snapshot (
    item_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    quantity_in_stock INT CHECK (quantity_in_stock >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO inventory_snapshot (product_name, category, quantity_in_stock) VALUES
('Wireless Mouse', 'Electronics', 150),
('Mechanical Keyboard', 'Electronics', 85),
('Ergonomic Chair', 'Furniture', 20),
('Monitor Stand', 'Accessories', 45),
('USB-C Cable', 'Electronics', 200);