# SocraCLV

### Group project within the scope of the course DS223 – Marketing Analytics

The project aims to develop a Python package for predicting a customer's Lifetime Value (CLV) for an Internet package provider that can be applied to similar-scope companies in general. As the name suggests, the package is not just about analytics but involves a philosophically flavoured approach to understanding and predicting Customer Lifetime Value to gain meaningful insights about the long-term relationships between the company and customers.

## SetUp

To get started, run 

```python -m clv.db.schema ``` to create the schema

```python basic_clv.py``` to load the data in the root of the repo

```python calculate_clv.py``` To calculate CLV and put into dataset
OR
```python -m clv.db.schema && python basic_clv.py && python calculate_clv.py```
and ```python -m clv.api.fast``` to run the api

To check the db follow the link https://inloop.github.io/sqlite-viewer/

### POST example of clv prediction table
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/clv/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'
```

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/clv/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"prediction_id": 9999,
"customer_id": 1,
"clv" :200,
"predicted_customer_type": "Lost Cause",
"is_campaign1_success": true,
"is_campaign2_success": true

}  '
```

### PUT example of clv prediction table
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/clv/10' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"clv" :200,
"predicted_customer_type": "Vulnerable Customer",
"is_campaign1_success": true,
"is_campaign2_success": true
}'
```

### DELETE example data from clv prediction table
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/clv/2' \
  -H 'accept: application/json'

```