USE testdb;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (name, city)
VALUES 
('Rahul', 'Mumbai'),
('Anita', 'Pune'),
('John', 'London');

SELECT * FROM customers;