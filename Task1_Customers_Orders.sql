SELECT name, SUM(amount) as total_spent, COUNT(*) as num_of_deal FROM customers
JOIN orders
ON orders.customer_id = customers.id
WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY name
HAVING SUM(amount) >= 30
ORDER BY SUM(amount) DESC;
