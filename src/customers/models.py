import helpers.billing
from django.db import models
from django.conf import settings
from allauth.account.signals import (user_signed_up as allauth_user_signed_up,
                                     email_confirmed as allauth_email_confirmed) 

User=settings.AUTH_USER_MODEL

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id=models.CharField(max_length=50, blank=True, null=True)
    init_email=models.EmailField(blank=True, null=True)
    init_email_confirmed=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            if self.init_email and self.init_email_confirmed:
              email=self.init_email
              if email != "" and email is not None:
                    stripe_id=helpers.billing.create_customer(email=email,raw=False)
                    self.stripe_id=stripe_id
        super().save(*args, **kwargs)