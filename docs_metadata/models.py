from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.core.exceptions import ValidationError


class Action(ChoiceEnum):
    ADD = 'ADD'
    ADD_NEXT = 'ADD_NEXT'
    END = 'END'
    CANCEL = 'CANCEL'
    HELP = 'HELP'


class ParseMode(ChoiceEnum):
    MARKDOWN = 'MARKDOWN'
    MARKDOWN_V2 = 'MARKDOWN_V2'
    HTML = 'HTML'


class Command(models.Model):
    action = EnumChoiceField(Action, default=Action.ADD_NEXT)
    name = models.CharField(max_length=256, unique=True, null=False)
    title = models.CharField(max_length=256, unique=True, null=False)
    prefix = models.CharField(max_length=256, unique=True, null=True, blank=True)

    def __str__(self):
        if self.prefix:
            return f'{self.title} ({self.name}:{self.prefix})'
        else:
            return f'{self.title} ({self.name})'


class CompanyWelcome(models.Model):
    help_command = models.ForeignKey(Command, on_delete=models.PROTECT, related_name="help_command")
    add_document_command = models.ForeignKey(Command, on_delete=models.PROTECT, related_name="add_document_command")
    add_next_document_command = models.ForeignKey(Command, on_delete=models.PROTECT,
                                                  related_name="add_next_document_command")
    end_document_command = models.ForeignKey(Command, on_delete=models.PROTECT, related_name="end_document_command")
    cancel_command = models.ForeignKey(Command, on_delete=models.PROTECT, related_name="cancel_command")

    readd_document_text = models.CharField(max_length=256)
    help_text = models.TextField(max_length=2048)
    start_text = models.TextField(max_length=2048)

    def save(self, *args, **kwargs):
        if not self.pk and CompanyWelcome.objects.exists():
            raise ValidationError('Company Welcome already exists')
        return super(CompanyWelcome, self).save(*args, **kwargs)


class Document(models.Model):
    order_index = models.IntegerField(null=False)
    file_prefix = models.CharField(max_length=256, null=False)
    index_text = models.CharField(max_length=5, null=True)
    text = models.TextField(max_length=512, null=True)
    buttons = models.ManyToManyField(Command, related_name="document_command")
    parse_mode = EnumChoiceField(ParseMode, default=ParseMode.MARKDOWN)
    remove_buttons_before_message = models.BooleanField(default=False)

    class Meta:
        ordering = ['order_index']
