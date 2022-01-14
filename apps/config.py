import json
import os
import xml.etree.ElementTree as et
from django.conf import settings


jpath = os.path.join(settings.BASE_DIR, './apps/permissions.json')
path = os.path.join(settings.BASE_DIR, './apps/config.xml')
tree = et.parse(path)
root = tree.getroot()

permissions = None
current_event_key = None
current_event_id = None
current_district_key = None

logged_in_users = []


def update_permissions():
    global permissions
    with open(jpath) as f:
        permissions = json.load(f)


update_permissions()
