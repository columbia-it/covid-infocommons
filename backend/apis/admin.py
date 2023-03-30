from django.contrib import admin
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from search.utils import update_person_in_grant_index, update_grant_in_grant_index
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

"""
Class to describe how Funder resource can be imported or exported:
"""
class FunderResource(resources.ModelResource):

    class Meta:
        model = Funder

"""
Class to describe how Grant resource can be imported or exported:
"""
class GrantResource(resources.ModelResource):
    
    funder = fields.Field(
        column_name='funder',
        attribute='funder',
        widget=ForeignKeyWidget(Funder, field='id'))
    
    program_officials = fields.Field(column_name='program_officials', attribute='program_officials', widget=ManyToManyWidget(Person, field='id'))
    
    principal_investigator = fields.Field(
        column_name='principal_investigator',
        attribute='principal_investigator',
        widget=ForeignKeyWidget(Person, field='id'))
    
    other_investigators = fields.Field(column_name='other_investigators', attribute='other_investigators', widget=ManyToManyWidget(Person, field='id'))
    
    awardee_organization = fields.Field(
        column_name='awardee_organization',
        attribute='awardee_organization',
        widget=ForeignKeyWidget(Organization, field='id'))
    
    class Meta:
        model = Grant
        import_id_fields = ('id',)
        fields = ('funder__id', 'id', 'award_id', 'title', 'program_officials__id', 'principal_investigator__id', 'awardee_organization__id', 'funder_divisions', 'program_reference_codes', 'start_date', 'end_date')
    

"""
ModelAdmin class to customize Person model view in Django admin
"""
class PersonAdmin(ImportExportModelAdmin):
    # Add filtering on fields
    list_filter = ('first_name', 'last_name',)
    # Add search on fields
    search_fields = ('first_name', 'id', 'last_name', 'emails',)

    # Override model save from admin so we can update the search index with these updates
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update search index
        update_person_in_grant_index(obj)

"""
ModelAdmin class to customize Grant model view in Django admin
"""
class GrantAdmin(ImportExportModelAdmin):
    # Add filtering on fields
    list_filter = ('principal_investigator__first_name', 'principal_investigator__last_name',)
    # Add search on fields
    search_fields = ('title', 'award_id', 'principal_investigator__first_name', 'principal_investigator__last_name')
    # Show the fields as inputs instead of drop-down lists to avoid overhead
    raw_id_fields = ('principal_investigator', 'awardee_organization', 'program_officials', 'other_investigators', 'funder')

    resource_classes = [GrantResource]

    # Override model save from admin so we can update the search index with these updates
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update search index
        update_grant_in_grant_index(obj)

"""
ModelAdmin class to customize Organization model view in Django admin
"""
class OrganizationAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('name', 'id', 'city', 'state',)


"""
ModelAdmin class to customize Publication model view in Django admin
"""
class PublicationAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)


"""
ModelAdmin class to customize Dataset model view in Django admin
"""
class DatasetAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)


"""
ModelAdmin class to customize Asset model view in Django admin
"""
class AssetAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'author__id', 'grant__id', 'publication__id',)


"""
ModelAdmin class to customize Funder model view in Django admin
"""
class FunderAdmin(ImportExportModelAdmin):
    resource_classes = [FunderResource]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Funder, FunderAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Asset, AssetAdmin)