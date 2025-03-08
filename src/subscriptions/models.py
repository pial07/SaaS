from django.db import models
from django.contrib.auth.models import Group,Permission
from django.db.models.signals import post_save

from django.conf import settings

User=settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS=True

SUBSCRIPTION_PERMISSION=[
               ("advanced","Advanced Perm"),
               ("basic","Basic Perm"),
               ("pro","Pro Perm"),
               ("basic_ai","Basic AI Perm"),
           ]

class Subscription(models.Model):
    name=models.CharField(max_length=120)
    active=models.BooleanField(default=True)
    groups=models.ManyToManyField(Group)
    permissions=models.ManyToManyField(Permission,limit_choices_to={
             "content_type__app_label": 'subscriptions',
             "codename__in":[x[0] for x in SUBSCRIPTION_PERMISSION]})

    class Meta:
           permissions=SUBSCRIPTION_PERMISSION

    def __str__(self):
        return f"{self.name}"

class UserSubscription(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE) 
    subscription=models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active=models.BooleanField(default=True)          
def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list("groups__id", flat=True)
        subs_groups_set = set(subs_groups)
        # groups_ids = groups.values_list('id', flat=True) # [1, 2, 3] 
        current_groups = user.groups.all().values_list('id', flat=True)
        current_groups_set = set(current_groups)
        current_groups_set.difference_update(subs_groups_set)
        current_groups_set.update(groups_ids)
        user.groups.set(list(current_groups_set))
post_save.connect(user_sub_post_save, sender=UserSubscription)   

# def user_sub_post_save(sender, instance, *args, **kwargs): 
#      user_sub_instance=instance
#      user=user_sub_instance.user
#      subscription_obj= user_sub_instance.subscription
#      groups=subscription_obj.groups.all()
#      if not ALLOW_CUSTOM_GROUPS:
#           user.groups.set(groups)
#      else:
#           subs_qs=Subscription.objects.filter(active=True).exclude(id=subscription_obj.id)
#           subs_groups=subs_qs.values_list("groups__id", flat=True)
#           subs_set=set(subs_groups)
#           group_ids=groups.values_list("id", flat=True)
#           current_groups=user.groups.all().values_list("id", flat=True)
#           group_ids_set=set(group_ids)
#           current_groups_set=set(current_groups)-subs_set
#           final_groups= list(group_ids_set | current_groups_set)
#           user.groups.set(final_groups)
          

