from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from docs_metadata.forms import CommandForm
from docs_metadata.models import Command
from docs_metadata.serializers import CommandSerializer


class CommandListView(LoginRequiredMixin, ListView):
    """"Список команд"""
    model = Command
    context_object_name = 'command_list'
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    template_name = 'docs_metadata/command_list.html'


class CommandCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Создание новой команды."""
    model = Command
    form_class = CommandForm
    template_name = 'docs_metadata/command_add.html'
    success_url = reverse_lazy('metadata_command_add')
    success_message = 'Команда успешно добавлена'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            command = form.save(commit=False)
            command.save()
            return self.form_valid(form)
        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response({'form': form})
