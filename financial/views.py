from financial.models import Transaction
from rest_framework import viewsets, status
from financial.serializers import TransactionSerializer, BalanceReportRequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from financial.serializers import BalanceReportRequestSerializer, BalanceReportResultSerializer
import django_filters.rest_framework
from rest_framework import filters, generics
from django.http import QueryDict


# Using ViewSet for CRUD >>>>>>>>
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'type', 'date']
    ordering_fields = ['amount', 'category', 'type', 'date']

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

    def create(self, request, *args, **kwargs):
        # TODO: Decorator for this functionality
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['wallet'] = request.user.wallet.id
        if isinstance(request.data, QueryDict):
            request.data._mutable = False

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('wallet') and request.data.get('wallet') != request.user.wallet.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['wallet'] = request.user.wallet.id  # wallet_id cannot be updated
        if isinstance(request.data, QueryDict):
            request.data._mutable = False

        return super().update(request, *args, **kwargs)


# Creating Generic View instead of API view for Better Documentation By Swagger
class BalanceReportAPIView(generics.RetrieveAPIView):
    serializer_class = BalanceReportRequestSerializer
    result_serializer_class = BalanceReportResultSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = BalanceReportRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        report = request.user.wallet.generate_date_interval_report(
            start_date=serializer.validated_data.get('start_date'),
            end_date=serializer.validated_data.get('end_date')
        )

        report_serialized = self.result_serializer_class(data=report)
        if report_serialized.is_valid():
            return Response(report_serialized.data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


