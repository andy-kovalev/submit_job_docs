from rest_framework import serializers

from docs_metadata.models import Command, CompanyWelcome, Document


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['id', 'action', 'name', 'title', 'prefix']


class CompanyWelcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWelcome
        fields = ['id', 'help_command', 'add_document_command', 'add_next_document_command', 'end_document_command',
                  'cancel_command', 'readd_document_text', 'help_text', 'start_text']

    def to_representation(self, instance):
        self.fields['help_command'] = CommandSerializer(read_only=True)
        self.fields['add_document_command'] = CommandSerializer(read_only=True)
        self.fields['add_document_command'] = CommandSerializer(read_only=True)
        self.fields['end_document_command'] = CommandSerializer(read_only=True)
        self.fields['cancel_command'] = CommandSerializer(read_only=True)

        return super(CompanyWelcomeSerializer, self).to_representation(instance)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'order_index', 'file_prefix', 'index_text', 'text', 'buttons', 'parse_mode',
                  'remove_buttons_before_message']

    def to_representation(self, instance):
        self.fields['buttons'] = CommandSerializer(read_only=True, many=True)

        return super(DocumentSerializer, self).to_representation(instance)
