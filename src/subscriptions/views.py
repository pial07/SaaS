import helpers.billing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse
from subscriptions.models import SubscriptionPrice,UserSubscription
from subscriptions import utils as subs_utils

@login_required
def user_subscription_view(request, *args, **kwargs):
    user_sub_obj, created=UserSubscription.objects.get_or_create(user=request.user)
    sub_data=user_sub_obj.serialize()
    if request.method == "POST":
        finished=subs_utils.refresh_active_users_subscription(user_ids=[request.user.id], active_only=False)
        if finished:
            messages.success(request, "Your plan detail refreshed")
        else:
            messages.error(request, "Your plan detail has not refreshed! Please try again")          
        return redirect(user_sub_obj.get_absolute_url())       
    return render(request, "subscriptions/user_detail_view.html", {"subscription": user_sub_obj})

@login_required
def user_subscription_cancel_view(request, *args, **kwargs):
    user_sub_obj, created=UserSubscription.objects.get_or_create(user=request.user)
    sub_data=user_sub_obj.serialize()
    if request.method == "POST":
        print("refresh sub")
        if user_sub_obj.stripe_id:
            sub_data=helpers.billing.cancel_subscription(user_sub_obj.stripe_id,
                                                         reason="user wanted to end",
                                                         feedback="other",
                                                         cancel_at_period_end=True,
                                                         raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj,k,v) 
            user_sub_obj.save() 
            messages.success(request, "Subscription cancelled") 
        return redirect(user_sub_obj.get_absolute_url())       
    return render(request, "subscriptions/user_cancel_view.html", {"subscription": user_sub_obj})

def subscription_price_view(request,interval="month"):
    qs= SubscriptionPrice.objects.filter(featured=True)
    inv_mo=SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr=SubscriptionPrice.IntervalChoices.YEARLY
    url_path="interval-pricing"
    mo_url=reverse(url_path,kwargs={"interval":inv_mo})
    yr_url=reverse(url_path,kwargs={"interval":inv_yr})
    active=inv_mo
    object_list= qs.filter(interval=inv_mo)
    if interval==inv_yr:
        object_list= qs.filter(interval=inv_yr)
        active=inv_yr
        
    return render(request, "subscriptions/pricing.html", {"object_list": object_list,
                                                          "mo_url":mo_url,"yr_url":yr_url,
                                                          "active":active,
                                                          
                                                          })
