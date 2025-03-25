
from typing import Any
from django.core.management.base import BaseCommand
from subscriptions import utils as subs_utils
class Command(BaseCommand):
    def add_arguments(self, parser):
      parser.add_argument("--clear-dangling", action="store_true", default=False)
    def handle(self, *args: Any, **options: Any):
        clear_dangling=options.get("clear_dangling")
        if clear_dangling:
           print("clearing dangling is not in active subs Stripe")
           subs_utils.clear_dangling_subs()
        else:
           print("Sync active subs")   
           done=subs_utils.refresh_active_users_subscription(active_only=True,verbose=True)
           if done:
             print("Done")
            
        