from django.template.defaulttags import register
from stepautomationapp.models import Documents

@register.filter
def splicestring(filestring, userlength):
    return filestring.name[userlength:]
