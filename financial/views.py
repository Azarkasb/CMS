from financial.models import Transaction
from rest_framework import viewsets, status
from financial.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from financial.serializers import BalanceReportRequestSerializer, BalanceReportResultSerializer


# Using ViewSet for CRUD >>>>>>>>
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['wallet'] = request.user.wallet.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['wallet'] = request.user.wallet.id     # wallet_id cannot be updated
        return super().update(request, *args, **kwargs)


class BalanceReportAPIView(APIView):

    def post(self, request):
        request_serializer = BalanceReportRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            start_date = request_serializer.validated_data['start_date']
            end_date = request_serializer.validated_data['end_date']

            raw_report = request.user.wallet.generate_date_interval_report(start_date, end_date)
            result_serializer = BalanceReportResultSerializer(data=raw_report)
            if result_serializer.is_valid():
                return Response(result_serializer.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)