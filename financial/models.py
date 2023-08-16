from django.db import models
from django.contrib.auth import get_user_model


class Wallet(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)



class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = "I", "income"
        EXPENSE = "E", "expense"

    class TransactionCategory(models.TextChoices):
        GROCERIES = "G", "groceries"
        UTILITIES = "U", "utilities"
        RENT = "R", "rent"
        MISC = "M", "misc"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    type = models.CharField(
        max_length=1,
        choices=TransactionType.choices
    )
    category = models.CharField(
        max_length=1,
        default=TransactionCategory.MISC,
        choices=TransactionCategory.choices
    )
    date = models.DateField(auto_now_add=True)


