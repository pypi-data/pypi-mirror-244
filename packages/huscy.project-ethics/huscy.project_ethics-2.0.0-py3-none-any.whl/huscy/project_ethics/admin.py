from django.contrib import admin
from reversion.admin import VersionAdmin

from huscy.project_ethics import models


@admin.register(models.EthicsCommittee)
class EthicsCommitteeAdmin(VersionAdmin, admin.ModelAdmin):
    pass


@admin.register(models.Ethics)
class EthicsAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = 'id', 'project_title', 'ethics_committee', 'code'
    search_fields = 'code', 'project__title'

    def project_title(self, ethics):
        return ethics.project.title


@admin.register(models.EthicsFile)
class EthicsFileAdmin(VersionAdmin, admin.ModelAdmin):
    date_hierarchy = "uploaded_at"
    fields = 'filetype', 'filehandle', 'filename'
    list_display = (
        'id',
        'ethics_code',
        'ethics_committee',
        'filename',
        'filetype',
        'project_title',
        'uploaded_at',
        'uploaded_by',
    )
    list_display_links = 'id', 'filename', 'filetype'
    readonly_fields = 'filehandle',
    search_fields = 'ethics__project__title', 'ethics__code', 'filename', 'uploaded_by'

    def has_add_permission(self, request, ethics_file=None):
        return False

    def ethics_committee(self, ethics_file):
        return ethics_file.ethics.ethics_committee.name

    def ethics_code(self, ethics_file):
        return ethics_file.ethics.code

    def project_title(self, ethics_file):
        return ethics_file.ethics.project.title
