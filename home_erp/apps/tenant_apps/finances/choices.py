"""Enums and choices for finances."""
from django.db import models

class AccountType(models.TextChoices):
    CHECKING = "CHECKING", "Checking"
    SAVINGS = "SAVINGS", "Savings"
    CREDIT_CARD = "CREDIT_CARD", "Credit Card"
    CASH = "CASH", "Cash"
    INVESTMENT = "INVESTMENT", "Investment"

class TransactionType(models.TextChoices):
    EXPENSE = "EXPENSE", "Expense"
    INCOME = "INCOME", "Income"
    TRANSFER = "TRANSFER", "Transfer"

