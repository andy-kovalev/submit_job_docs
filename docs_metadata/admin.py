from django.contrib import admin

from docs_metadata import models


@admin.register(models.Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('action', 'name', 'title', 'prefix',)
    list_filter = ('action',)
    search_fields = ('action', 'name', 'title',)


@admin.register(models.CompanyWelcome)
class CompanyWelcomeAdmin(admin.ModelAdmin):
    list_display = (
        'help_command', 'add_document_command', 'add_next_document_command', 'end_document_command', 'cancel_command',
        'readd_document_text', 'help_text', 'start_text',)


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('order_index', 'file_prefix', 'index_text', 'text', 'parse_mode', 'remove_buttons_before_message',)
    list_filter = ('index_text', 'text',)
    search_fields = ('index_text', 'text', 'buttons', 'parse_mode',)
    filter_horizontal = ('buttons',)
