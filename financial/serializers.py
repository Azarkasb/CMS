from rest_framework import serializers
from financial.models import Transaction
from datetime import date


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BalanceReportRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        if not data.get('start_date') and not data.get('end_date'):
            data['start_date'] = date.today().replace(day=1)
            data['end_date'] = date.today()

        if not data.get('start_date') or not data.get('end_date'):
            raise serializers.ValidationError("providing only one of start_date, end_date fields is not allowed")

        return data


class BalanceReportResultSerializer(serializers.Serializer):
    total_income = serializers.IntegerField()
    total_expense = serializers.IntegerField()
    current_balance = serializers.IntegerField()

    net_cash_flow = serializers.SerializerMethodField()
    initial_balance = serializers.SerializerMethodField()

    def get_net_cash_flow(self, obj):
        return obj['total_income'] - obj['total_expense']

    def get_initial_balance(self, obj):
        # we supposed to calculate it again
        total_cash_flow = obj['total_income'] - obj['total_expense']
        return obj['current_balance'] - total_cash_flow
