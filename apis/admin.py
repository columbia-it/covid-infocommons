from django.contrib import admin
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset

admin.site.register(Organization)
admin.site.register(Person)
admin.site.register(Grant)
admin.site.register(Funder)
admin.site.register(Publication)
admin.site.register(Dataset)
admin.site.register(Asset)