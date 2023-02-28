from django.contrib import admin
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset


"""
ModelAdmin class to customize Person model view in Django admin
"""
class PersonAdmin(admin.ModelAdmin):
    # Add filtering on fields
    list_filter = ('first_name', 'last_name',)
    # Add search on fields
    search_fields = ('first_name', 'id', 'last_name', 'emails',)


"""
ModelAdmin class to customize Grant model view in Django admin
"""
class GrantAdmin(admin.ModelAdmin):
    # Add filtering on fields
    list_filter = ('principal_investigator__first_name', 'principal_investigator__last_name',)
    # Add search on fields
    search_fields = ('title', 'award_id', 'principal_investigator__first_name', 'principal_investigator__last_name')
    # Show the fields as inputs instead of drop-down lists to avoid overhead
    raw_id_fields = ('principal_investigator', 'awardee_organization', 'program_officials', 'other_investigators', 'funder')


"""
ModelAdmin class to customize Organization model view in Django admin
"""
class OrganizationAdmin(admin.ModelAdmin):
    # Add search on fields
    search_fields = ('name', 'id', 'city', 'state',)


"""
ModelAdmin class to customize Publication model view in Django admin
"""
class PublicationAdmin(admin.ModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)


"""
ModelAdmin class to customize Dataset model view in Django admin
"""
class DatasetAdmin(admin.ModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)


"""
ModelAdmin class to customize Asset model view in Django admin
"""
class AssetAdmin(admin.ModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'author__id', 'grant__id', 'publication__id',)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Funder)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Asset, AssetAdmin)