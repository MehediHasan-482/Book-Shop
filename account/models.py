from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.core.exceptions import ValidationError


class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('silver', 'Silver - 3 months'),
        ('gold', 'Gold - 6 months'),
        ('platinum', 'Platinum - 12 months'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    amount = models.CharField(max_length=20)  
    account_number = models.CharField(max_length=20, verbose_name="Account Number")

    # def clean(self):
    #     # Validate that account_number is exactly 11 digits
    #     if len(str(self.account_number)) != 11:
    #         raise ValidationError("Account number must be exactly 11 digits.")

    def save(self, *args, **kwargs):
        # Ensure start_date is set properly
        if not self.start_date:
            self.start_date = date.today()

        # Calculate end_date and amount based on subscription_type
        if self.subscription_type == 'silver':
            self.end_date = self.start_date + timedelta(days=90)
            self.amount = 50  # Amount for Silver plan
        elif self.subscription_type == 'gold':
            self.end_date = self.start_date + timedelta(days=180)
            self.amount = 90  # Amount for Gold plan
        elif self.subscription_type == 'platinum':
            self.end_date = self.start_date + timedelta(days=365)
            self.amount = 150  # Amount for Platinum plan

        # Call the parent save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type.capitalize()}"
