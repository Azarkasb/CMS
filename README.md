# CMS
Cash Management System

## APIs

### Auth

#### REGISTER /register/
curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:8000/register/

#### LOGIN /api-token-auth/


### Financial
#### GET /financial/transactions
curl -X GET  -H 'Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55' http://127.0.0.1:8000/financial/transactions/

#### POST /financial/transactions/
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/

result: created with id {id}

#### DELETE /financial/transactions/{id}/
curl -X DELETE -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55"  http://127.0.0.1:8000/financial/transactions/1/

#### PATCH /financial/transactions/{id}/
partial update
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/2/

#### PUT /financial/transactions/{id}/
full update