from django.contrib import admin
from .models import Organization, Person, Grant, Funder

admin.site.register(Organization)
admin.site.register(Person)
admin.site.register(Grant)
admin.site.register(Funder)