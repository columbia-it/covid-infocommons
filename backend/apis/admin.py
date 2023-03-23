from django.contrib import admin
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from search.utils import update_person_in_grant_index, update_grant_in_grant_index
from import_export import resources
from import_export.admin import ImportExportModelAdmin

"""
Class to describe how Person resource can be imported or exported:
"""
class PersonResource(resources.ModelResource):

    class Meta:
        model = Person


"""
Class to describe how Organization resource can be imported or exported:
"""
class OrganizationResource(resources.ModelResource):

    class Meta:
        model = Organization

    
"""
Class to describe how Grant resource can be imported or exported:
"""
class GrantResource(resources.ModelResource):

    class Meta:
        model = Grant


"""
Class to describe how Funder resource can be imported or exported:
"""
class FunderResource(resources.ModelResource):

    class Meta:
        model = Funder


"""
Class to describe how Publication resource can be imported or exported:
"""
class PublicationResource(resources.ModelResource):

    class Meta:
        model = Publication


"""
Class to describe how Dataset resource can be imported or exported:
"""
class DatasetResource(resources.ModelResource):

    class Meta:
        model = Dataset


"""
Class to describe how Asset resource can be imported or exported:
"""
class AssetResource(resources.ModelResource):

    class Meta:
        model = Asset


"""
ModelAdmin class to customize Person model view in Django admin
"""
class PersonAdmin(ImportExportModelAdmin):
    # Add filtering on fields
    list_filter = ('first_name', 'last_name',)
    # Add search on fields
    search_fields = ('first_name', 'id', 'last_name', 'emails',)
    resource_classes = [PersonResource]

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

    # Override model save from admin so we can update the search index with these updates
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update search index
        update_grant_in_grant_index(obj)

    resource_classes = [GrantResource]


"""
ModelAdmin class to customize Organization model view in Django admin
"""
class OrganizationAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('name', 'id', 'city', 'state',)
    resource_classes = [OrganizationResource]


"""
ModelAdmin class to customize Publication model view in Django admin
"""
class PublicationAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)
    resource_classes = [PublicationResource]


"""
ModelAdmin class to customize Dataset model view in Django admin
"""
class DatasetAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'title', 'grants__id',)
    resource_classes = [DatasetResource]


"""
ModelAdmin class to customize Asset model view in Django admin
"""
class AssetAdmin(ImportExportModelAdmin):
    # Add search on fields
    search_fields = ('doi', 'id', 'author__id', 'grant__id', 'publication__id',)
    resource_classes = [AssetResource]


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