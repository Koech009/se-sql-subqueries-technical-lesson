import sqlite3
import pandas as pd
conn = sqlite3.Connection('data.sqlite')

q = """
SELECT lastName,firstName, officeCode
FROM employees
JOIN offices
    USING (officeCode)
WHERE country = 'USA';
"""
# print(pd.read_sql(q, conn))
# subsitute  the join with a subquery
q = """
SELECT lastName,firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    WHERE country = 'USA'
);
"""
# print(pd.read_sql(q, conn))
# subquery for filtering based on an aggregatation
q = """SELECT lastName,firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    JOIN employees
        USING (officeCode)
    GROUP BY 1
    HAVING COUNT(employeeNumber) >= 5
);"""
print(pd.read_sql(q, conn))
# chaining aggregates
q = """
SELECT AVG(customerAvgPayment) AS averagePayment
FROM (
    SELECT AVG(amount) AS customerAvgPayment
    FROM payments
    JOIN customers
        USING(customerNumber)
    GROUP BY customerNumber
)
;"""
pd.read_sql(q, conn)

q = """
SELECT lastName, firstName, employeeNumber
FROM employees
WHERE employeeNumber IN (SELECT salesRepEmployeeNumber
                     FROM customers 
                     WHERE country = "USA")
;
"""
pd.read_sql(q, conn)
conn.close()
