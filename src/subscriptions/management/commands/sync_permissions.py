from typing import Any
from django.core.management.base import BaseCommand

from subscriptions import utils as subs_utils
class Command(BaseCommand):
    def add_arguments(self, parser):
      parser.add_argument("--clear-dangling", action="store_true", default=False)

    def handle(self, *args: Any, **options: Any):
        print(options)
        subs_utils.sync_subs_group_permissions()