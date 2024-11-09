--PRODUCTS QUERIES--
--View monthly order totals:
--Write a query that totals all the orders in the classic models database and groups the results by month and year.
CREATE OR REPLACE VIEW monthlyOrderTotals AS
SELECT YEAR(orderDate) AS orderYear, MONTHNAME(orderDate) AS orderMonth, SUM(quantityOrdered * priceEach) AS totalOrderValue
FROM orders
JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
GROUP BY orderYear, orderMonth, MONTH(orderDate)
ORDER BY MONTH(orderDate);

--View order totals by product line:
--Write a query that totals all the orders in the classic models database and groups the results by order line and year.
CREATE OR REPLACE VIEW totalsByProductLine AS
SELECT YEAR(orderDate) AS orderYear, productLine, SUM(quantityOrdered * priceEach) AS totalOrderValue
FROM orders
JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
JOIN products ON orderdetails.productCode = products.productCode
GROUP BY orderYear, productLine
ORDER BY productLine;

--View order totals by product:
--Write a query that totals all the orders in the classic models database and groups the results by product name and year.
CREATE OR REPLACE VIEW totalsByProduct AS
SELECT YEAR(o.orderDate) AS orderYear, p.productName, SUM(od.quantityOrdered * od.priceEach) AS totalOrderValue
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
GROUP BY orderYear, p.productName
ORDER BY totalOrderValue DESC;

--CUSTOMERS QUERIES--
--View order totals by customer:
--Write a query that totals all the customer orders in the classic models database and groups the results by customer and year.
CREATE OR REPLACE VIEW customerOrderTotals AS
SELECT c.customerName, YEAR(o.orderDate) AS orderYear, SUM(od.quantityOrdered * od.priceEach) AS totalOrder
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY c.customerName, orderYear
ORDER BY totalOrder DESC;

--View total payments by customer:
--Write a query that totals all the payments by customer in the classic models database and groups the results by customer and year.
CREATE OR REPLACE VIEW customerPayments AS
SELECT c.customerName, YEAR(p.paymentDate) AS paymentYear, SUM(p.amount) AS totalPayment
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY c.customerName, paymentYear
ORDER BY totalPayment DESC;


--EMPLOYEES QUERIES--
--View employee order totals:
--Write a query that totals all the orders an employee is responsible for in the classic models database and groups the results by employee and year.
CREATE OR REPLACE VIEW employeeOrderTotals AS
SELECT CONCAT(e.firstName, ' ', e.lastName) AS employeeName, YEAR(o.orderDate) AS orderYear, SUM(od.quantityOrdered * od.priceEach) AS totalOrderValue
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY employeeName, orderYear
ORDER BY totalOrderValue DESC, employeeName;

--View employee number of orders:
--Write a query that counts the number of orders an employee is responsible for in the classic models database and groups the results by employee and year.
CREATE OR REPLACE VIEW employeeNumOfOrders AS
SELECT CONCAT(e.firstName, ' ', e.lastName) AS employeeName, YEAR(o.orderDate) AS orderYear, COUNT(o.orderNumber) AS totalOrders
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY employeeName, orderYear
ORDER BY totalOrders DESC, employeeName;
