from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financial.views import TransactionViewSet, BalanceReportAPIView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('report/', BalanceReportAPIView.as_view())
]