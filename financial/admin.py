from django.contrib import admin
from financial.models import Wallet, Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)
