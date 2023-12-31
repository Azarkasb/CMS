from django.db import models
from django.contrib.auth import get_user_model
import datetime as dt


class Wallet(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)

    def generate_date_interval_report(self, start_date: dt.date, end_date: dt.date):
        transactions = self.transaction_set.filter(date__range=[start_date, end_date])
        report = dict()
        report.update(transactions.filter(type="I").aggregate(total_income=models.Sum('amount')))
        if report.get("total_income") is None:
            report["total_income"] = 0

        report.update(transactions.filter(type="E").aggregate(total_expense=models.Sum('amount')))
        if report.get("total_expense") is None:
            report["total_expense"] = 0

        report.update({'current_balance': self.balance})

        return report


class Transaction(models.Model):
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
    date = models.DateField(default=dt.date.today)

    def apply_balance_effect(self, reverse=False):
        value = self.amount if self.type == "I" else -1 * self.amount
        if reverse:
            value *= -1

        self.wallet.balance += value
        self.wallet.save()

    def save(self, *args, **kwargs):
        if self.pk:  # update time
            previous_transaction = Transaction.objects.get(pk=self.pk)
            previous_transaction.apply_balance_effect(reverse=True)
        self.apply_balance_effect()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.apply_balance_effect(reverse=True)
        super().delete(*args, **kwargs)
