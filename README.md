# up2149569_m31882_frontend

This is the frontend code base for the end-to-end trading bot using Python.

For security purposes, the secret.py has been truncated. Do fill it in with your own database's credentials.

The code to create the SQL table is as follow:

```sql
CREATE TABLE `users` (
  	`api_key` varchar(50) NOT NULL,
 	 `secret_key` varchar(50) NOT NULL,
  	`days_to_trade` varchar(10) NOT NULL DEFAULT '0',
 	 `email` varchar(255) DEFAULT NULL,
  	`date_submitted` date DEFAULT NULL,
  	PRIMARY KEY (`api_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```
