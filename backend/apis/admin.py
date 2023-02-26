from django.contrib import admin
from .models import Organization, Funder, Person, Grant, Publication, Dataset, Asset


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]


class FunderAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['id', 'first_name', 'last_name', 'emails',]


class GrantAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title',]


class PublicationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title']


class DatasetAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title']


class AssetAdmin(admin.ModelAdmin):
    search_fields = ['id', 'filename']
    
 
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Funder, FunderAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Asset, AssetAdmin)
