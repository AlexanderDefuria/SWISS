import json
import os
import xml.etree.ElementTree as et
import dbTools
from apps.entry.models import Event
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


def update_from_xml():
    global current_event_key, current_district_key, current_event_id, tree, root
    tree = et.parse(path)
    root = tree.getroot()
    current_event_key = root.find('events/current-event').text
    current_district_key = root.find('events/district-key').text
    current_event_id = dbTools.event_id_lookup(current_event_key)


def get_current_event_key():
    update_from_xml()
    return current_event_key


def get_current_event_id():
    update_from_xml()
    return current_event_id


def get_current_district_key():
    update_from_xml()
    return current_district_key


def set_event(FIRST_key):
    """
    :param FIRST_key: The FIRST Key of the Event
    """
    global current_event_key, current_event_id, root
    current_event_key = root.find('events/current-event').text = FIRST_key
    current_event_id = Event.objects.filter(FIRST_key=current_event_key)[0].id
    write_changes()


def set_district(FIRST_key):
    """
    :param FIRST_key: The FIRST Key of the District
    """
    global current_district_key, root
    current_district_key = root.find('events/district-key').text = FIRST_key
    write_changes()


def write_changes():
    global tree, path
    tree.write(path)


update_from_xml()
update_permissions()
