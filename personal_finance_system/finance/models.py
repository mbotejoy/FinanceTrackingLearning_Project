from django.conf import settings
from django.db import models


class Category(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="budgets"
    )

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "budgets"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} - {self.amount}"


class SavingsGoal(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("paused", "Paused"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="savings_goals"
    )

    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    target_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "savings_goals"
        ordering = ["target_date"]

    def __str__(self):
        return self.name