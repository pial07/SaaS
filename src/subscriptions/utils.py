import helpers.billing
from typing import Any
from django.core.management.base import BaseCommand
from django.db.models import Q
from customers.models import Customer
from subscriptions.models import UserSubscription,Subscription,SubscriptionStatus

def refresh_active_users_subscription(user_ids=None, active_only=True,verbose=False):
     
     qs=UserSubscription.objects.all()
     if active_only:
          qs=qs.by_active_trialing()
     if user_ids is not None:
          qs=qs.by_user_ids(user_ids=user_ids)
     complete_count=0
     qs_count=qs.count()             
     for obj in qs:
        if verbose:
             print("Updating User",obj.user,obj.subscription,obj.current_period_end)
        if obj.stripe_id:
                sub_data=helpers.billing.get_subscription(obj.stripe_id,raw=False)
                for k,v in sub_data.items():
                    setattr(obj,k,v)
                obj.save()
                complete_count+=1
     return complete_count == qs_count          

def clear_dangling_subs():
        qs= Customer.objects.filter(stripe_id__isnull=False)
        for customer_obj in qs:
            user=customer_obj.user
            customer_stripe_id=customer_obj.stripe_id
            print(f"Sync {user}-{customer_stripe_id} subs and remove old ones")
            subs=helpers.billing.get_customer_active_subscription(customer_stripe_id)
            for sub in subs:
                existing_user_sub_qs=UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
                if existing_user_sub_qs.exists():
                    continue
                helpers.billing.cancel_subscription(sub.id,reason="Dangling user Subscription",                    cancel_at_period_end=False)
                print(sub.id, existing_user_sub_qs.exists())
            

def sync_subs_group_permissions():
        qs= Subscription.objects.filter(active=True)
        for obj in qs:
            set_perms= obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(set_perms)    