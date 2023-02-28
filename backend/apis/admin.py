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


admin.site.register(Organization)
admin.site.register(Person, PersonAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Funder)
admin.site.register(Publication)
admin.site.register(Dataset)
admin.site.register(Asset)