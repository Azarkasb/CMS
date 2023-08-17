# CMS
### Cash Management System

*Quera Mentorship Task*

## Deploy
### Production
make sure docker and docker compose has been correctly installed
move to the project root directory (CMS) and run 
> docker compose up

then run
> docker exec cms-web-1 python manage.py migrate

*optional*  for having access to admin pages
> docker exec -it cms-web-1 python manage.py createsuperuser

---

## APIs

### Auth

### REGISTER 

+ method: **POST**
+ endpoint: **/register/**

+   example:
    > ```curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:8000/register/```

  +   result:
    >  {"token":"c2ca088287bf5681f80e778c23151b3e3610f4d6"}

### LOGIN /api-token-auth/

example:
> ```curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:8000/register/```

result:
> {"token":"c2ca088287bf5681f80e778c23151b3e3610f4d6"}

### Financial

### GET /financial/transactions

example:
> ```curl -X GET  -H 'Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55' http://127.0.0.1:8000/financial/transactions/```


### POST /financial/transactions/

example:
> ```curl -X POST -H "Content-Type: application/json" -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/```


### DELETE /financial/transactions/{id}/

example:
> ```curl -X DELETE -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55"  http://127.0.0.1:8000/financial/transactions/1/```


### PATCH /financial/transactions/{id}/

+ example:
    > ```curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/2/```

### FULLY UPDATE DETAILS OF A TRANSACTION 
+   method: **PUT**
  + endpoint: **/financial/transactions/{id}/**
+   example:
    > ```curl -X PUT -H "Content-Type: application/json" -H "Authorization: Token 9d3e4c1156508cb3ebde92ff500de9a7ba986b55" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/3/```


### Generate REPORT: 
+ method: **POST**
+ endpoint: **/financial/report/**
+   example:
    > ```curl -X POST -H "Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6" http://0.0.0.0:8000/financial/report/```

+   result:
    > {"total_income":0,"total_expense":0,"current_balance":0,"net_cash_flow":0,"initial_balance":0}