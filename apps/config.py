import json
import os
from django.conf import settings

jpath = os.path.join(settings.BASE_DIR, './apps/permissions.json')

permissions = None

logged_in_users = []


def update_permissions():
    global permissions
    with open(jpath) as f:
        permissions = json.load(f)


update_permissions()
