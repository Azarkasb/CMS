from financial.models import Transaction
from rest_framework import viewsets, status
from financial.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from financial.serializers import BalanceReportRequestSerializer, BalanceReportResultSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        data['wallet'] = request.user.wallet.id
        data._mutable = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(f"created with id {serializer.data.get('id')}", status=status.HTTP_201_CREATED)


class BalanceReportAPIView(APIView):

    def post(self, request):
        request_serializer = BalanceReportRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            start_date = request_serializer.validated_data['start_date']
            end_date = request_serializer.validated_data['end_date']

            raw_report = request.user.wallet.generate_date_interval_report(start_date, end_date)
            print(raw_report)
            result_serializer = BalanceReportResultSerializer(data=raw_report)
            if result_serializer.is_valid():
                return Response(result_serializer.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)