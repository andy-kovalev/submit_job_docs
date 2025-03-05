from django import forms
from enumchoicefield import forms as ecf_forms

from .models import Command, CompanyWelcome, Document


class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['action', 'name', 'title', 'prefix']

        widgets = {'action': ecf_forms.EnumSelect(members=('ADD', 'ADD_NEXT', 'END', 'CANCEL', 'HELP'),
                                                  attrs={'class': 'form-control', 'placeholder': 'Действие'}),
                   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование'}),
                   'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
                   'prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Префикс файла'}), }


class CompanyWelcomeForm(forms.ModelForm):
    class Meta:
        model = CompanyWelcome
        fields = ['help_command', 'add_document_command', 'add_next_document_command', 'end_document_command',
                  'cancel_command', 'readd_document_text', 'help_text', 'start_text']

        widgets = {
            'help_command': forms.Select(attrs={"class": "form-control", }),
            'add_document_command':  forms.Select(attrs={"class": "form-control", }),
            'add_next_document_command':  forms.Select(attrs={"class": "form-control", }),
            'end_document_command':  forms.Select(attrs={"class": "form-control", }),
            'cancel_command':  forms.Select(attrs={"class": "form-control", }),
            'readd_document_text': forms.TextInput(attrs={'class': 'form-control', }),
            'help_text': forms.Textarea(attrs={'class': 'form-control', }),
            'start_text': forms.TextInput(attrs={'class': 'form-control', }), }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['order_index', 'file_prefix', 'index_text', 'text', 'parse_mode', 'remove_buttons_before_message']

        widgets = {'order_index': forms.TextInput(attrs={'class': 'form-control', }),
                   'file_prefix': forms.TextInput(attrs={'class': 'form-control', }),
                   'index_text': forms.TextInput(attrs={'class': 'form-control', }),
                   'text': forms.Textarea(attrs={'class': 'form-control', }),
                   'parse_mode': ecf_forms.EnumSelect(attrs={'class': 'form-control'}),
                   'remove_buttons_before_message': forms.CheckboxInput(attrs={"class": "form-control", }), }
