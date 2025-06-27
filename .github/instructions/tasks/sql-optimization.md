---
applyTo: ["sql", "bigquery", "optimization", "data-engineering", "performance"]
description: "Instructions for SQL query optimization in BigQuery and data modeling"
priority: "high"
---

# **Task: SQL Optimization and Data Modeling (BigQuery)**

When working with SQL in BigQuery, follow these optimization practices and data modeling principles.

## **BigQuery SQL Optimization Rules**

### **1. Query Structure Optimization**
- **Use SELECT only needed columns**: Avoid `SELECT *` especially on wide tables
- **Apply filters early**: Use `WHERE` clauses before `JOIN` operations
- **Limit data processed**: Use `LIMIT` for exploratory queries
- **Partition pruning**: Always filter on partition columns when available

### **2. JOIN Optimization**
- **Use appropriate JOIN types**: INNER, LEFT, RIGHT, FULL OUTER based on data relationships
- **Join on clustered columns**: Leverage table clustering for better performance
- **Broadcast joins**: Use `/*+ BROADCAST(table) */` hint for small dimension tables
- **Avoid cross joins**: Unless absolutely necessary for analytical purposes

### **3. Window Functions Best Practices**
- **Use PARTITION BY wisely**: Partition on columns that reduce data movement
- **Combine window functions**: Use multiple functions in single OVER clause when possible
- **Order by performance**: Consider the cost of ORDER BY in window functions

## **Data Modeling Standards**

### **1. Table Design**
- **Partition tables** on date/datetime columns (daily partitioning recommended)
- **Cluster tables** on frequently filtered columns (up to 4 clustering columns)
- **Denormalize appropriately**: Balance between query performance and storage costs
- **Use nested and repeated fields**: For complex data structures

### **2. Schema Design**
- **Consistent naming conventions**: Use snake_case for all objects
- **Descriptive column names**: Avoid abbreviations, use clear business terms
- **Data types optimization**: Use appropriate types (INT64 vs FLOAT64, STRING vs BYTES)
- **Required vs nullable**: Set appropriate field modes based on business rules

### **3. Performance Patterns**
```sql
-- Good: Partition pruning with date filter
SELECT customer_id, order_amount, order_date
FROM `project.dataset.orders`
WHERE order_date >= '2023-01-01'
  AND order_date < '2024-01-01'
  AND customer_region = 'US'

-- Good: Efficient aggregation with early filtering
SELECT 
  customer_id,
  COUNT(*) as order_count,
  SUM(order_amount) as total_amount
FROM `project.dataset.orders`
WHERE order_date >= CURRENT_DATE() - 90
GROUP BY customer_id
HAVING COUNT(*) >= 5
```

## **Common Anti-Patterns to Avoid**

### **1. Performance Killers**
- ❌ Using `ORDER BY` without `LIMIT`
- ❌ `SELECT DISTINCT` on large datasets without proper filtering
- ❌ Unnecessary `GROUP BY` operations
- ❌ Cross joins without proper conditions

### **2. Cost Inefficiencies**
- ❌ Processing entire tables when time-based filtering is possible
- ❌ Using `SELECT *` in production queries
- ❌ Repeated similar queries instead of materialized views
- ❌ Not using approximate aggregation functions when exact precision isn't needed

## **Data Quality Validation Patterns**

```sql
-- Data quality checks template
WITH data_quality_checks AS (
  SELECT
    -- Completeness checks
    COUNT(*) as total_records,
    COUNT(customer_id) as non_null_customers,
    COUNT(DISTINCT customer_id) as unique_customers,
    
    -- Range checks
    MIN(order_date) as earliest_date,
    MAX(order_date) as latest_date,
    
    -- Business rule validation
    SUM(CASE WHEN order_amount < 0 THEN 1 ELSE 0 END) as negative_amounts,
    SUM(CASE WHEN order_date > CURRENT_DATE() THEN 1 ELSE 0 END) as future_dates
    
  FROM `project.dataset.orders`
  WHERE order_date >= CURRENT_DATE() - 1
)
SELECT * FROM data_quality_checks;
```

## **Documentation Requirements**

- **Query purpose**: Comment explaining the business logic
- **Performance considerations**: Document expected data volume and execution time
- **Data lineage**: Specify source tables and transformations
- **Maintenance notes**: Include refresh frequency and dependencies

## **Code Standards**

- **Indentation**: Use 2 spaces for SQL indentation
- **Capitalization**: SQL keywords in UPPER CASE, identifiers in snake_case
- **Comments**: Use `--` for single line, `/* */` for multi-line comments
- **Line length**: Keep lines under 100 characters when possible
