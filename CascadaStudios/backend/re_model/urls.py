from django.urls import path
from django.contrib import admin

from .views import (
    home,
    income_page,
    expense_page,
    uses_page,
    loan_page,
    cash_flow_page,
    pnl_page
)

urlpatterns = [
    path("", home, name="home"), # need to specifiy name arg
    path("income", income_page),
    path("expense", expense_page),
    path("uses", uses_page),
    path("loan", loan_page),
    path("cf", cash_flow_page),
    path("pnl", pnl_page),
]
