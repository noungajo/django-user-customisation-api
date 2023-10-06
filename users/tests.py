from django.test import TestCase

import requests

endpoint = "http://127.0.0.1:8000/user/users/register"
response = requests.post(endpoint,json={
  "full_name": "string",
  "date_of_birth": "2023-07-31",
  "email": "user@example.com",
  "numero_social": "string",
  "address": "string",
  "telephone": "string",
  "password": "string",
  "remuneration": "mensuel",
  "base_salary": 0
})
print(response.json())
print(response.status_code)
#HTTP REQUEST --> html
#rest api http --> json:javascript object notation
