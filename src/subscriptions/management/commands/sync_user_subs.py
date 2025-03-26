
from typing import Any
from django.core.management.base import BaseCommand
from subscriptions import utils as subs_utils
class Command(BaseCommand):
    def add_arguments(self, parser):
      parser.add_argument("--day-start", type=int, default=0)
      parser.add_argument("--day-end", type=int, default=0)
      parser.add_argument("--days-left", type=int, default=0)
      parser.add_argument("--days-ago", type=int, default=0)
      parser.add_argument("--clear-dangling", action="store_true", default=False)
  
    def handle(self, *args: Any, **options: Any):
        clear_dangling=options.get("clear_dangling")
        day_start=options.get("day_start")
        day_end=options.get("day_end")
        days_left=options.get("days_left")
        days_ago=options.get("days_ago")
        if clear_dangling:
           print("clearing dangling is not in active subs Stripe")
           subs_utils.clear_dangling_subs()
        else:
           print("Sync active subs")   
           done=subs_utils.refresh_active_users_subscription(active_only=True,
                                                             days_left=days_left,
                                                             days_ago=days_ago,
                                                             day_start=day_start,
                                                             day_end=day_end, 
                                                             verbose=True)
           if done:
             print("Done")
            
        