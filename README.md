# CMS
### Cash Management System

*Quera Mentorship Task*

## Deploy
### Production
make sure docker and docker compose has been correctly installed
move to the project root directory (CMS) and run 
> docker compose build

> docker compose up

then run
> docker exec cms-web-1 python manage.py migrate

*optional*  for having access to admin pages
> docker exec -it cms-web-1 python manage.py createsuperuser

---

## APIs
**note**: substitute token value and your host with what have been used in the given examples

**note**: To use apis with authentication first register or login and include your token in the header (just like examples) for subsequent requests

### Auth

### REGISTER 

+ method: **POST**
+ endpoint: **/register/**

+   example:
    > ```curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:8000/register/```

  +   result:
    >  {"token":"c2ca088287bf5681f80e778c23151b3e3610f4d6"}

### LOGIN

+   method: **POST**
  + endpoint: **/api-token-auth/**

+   example:
    > ```curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}' http://127.0.0.1:8000/api-token-auth/```

+   result:
    > {"token":"c2ca088287bf5681f80e778c23151b3e3610f4d6"}

### Financial

### Retrieve list of user transactions

+   method: **GET**
  + endpoint: **/financial/transactions/**

  + customize filtering and sorting with query parameters
    + filter results
      + /financial/transactions/?type=I or /financial/transactions/?type=E (I for Income, E for Expense)
      + /financial/transactions/?date=2022-03-12 (use your arbitrary date)
      + /financial/transactions/?category=G (G for groceries, U for Utilities, M for Misk, R for Rent)

    + sort results
      + /financial/transactions/?ordering=type (date or category or amount)
      + /financial/transactions/?ordering=-amount (you can use - before option for reverse ordering)

+   example:
    > ```curl -X GET  -H 'Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6' http://127.0.0.1:8000/financial/transactions/?ordering=-amount```

  + result
    > list of transactions with details

### Create Transaction

+   method: **POST**
+ endpoint: **/financial/transactions/**

+   example:
    > ```curl -X POST -H "Content-Type: application/json" -H "Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/```
  + result
    > {"id":1,"amount":10000,"type":"I","category":"M","date":"2023-08-18","wallet":1}

### Delete transaction 

+   method: **DELETE**
+ endpoint: **/financial/transactions/{id}**

+   example:
    > ```curl -X DELETE -H "Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6"  http://127.0.0.1:8000/financial/transactions/1/```
+ result
  > No Result :)


### Update Transaction
+   method: **PUT**
+ endpoint: **/financial/transactions/{id}**

+   example:
    > ```curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6" -d '{"type": "I", "amount": 10000}' http://127.0.0.1:8000/financial/transactions/2/```
+ result
  > {"id":2,"amount":10000,"type":"I","category":"M","date":"2023-08-18","wallet":1}


### Generate REPORT: 
+ method: **GET**
+ endpoint: **/financial/report/**
+ customize start_date and end_date using query_params
  + you can decide to provide either start_date and end_date or let the Application set it
    + /financial/report/?start_date=2023-08-19&end_date=2023-03-15  (default is first day of the current month)
    + providing only one of them is not allowed
+   example:
    > ```curl -X GET -H "Authorization: Token c2ca088287bf5681f80e778c23151b3e3610f4d6" "http://0.0.0.0:8000/financial/report/?start_date=2000-02-02&end_date=2023-08-18"```

+   result:
    > {"total_income":50000,"total_expense":0,"current_balance":70000,"net_cash_flow":50000,"initial_balance":20000}
